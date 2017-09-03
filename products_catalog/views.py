import json
from json import JSONDecodeError

from django.views import View
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from customer_profile.models import Profile
from orders.models import Order, OrderLineItem
from entity_management.models import ProductTier

from orders.tasks import set_order_to_expire, mail_customer_now


class ProductCatalogView(View):
    @staticmethod
    def get(request):
        return render(request, 'products_catalog.html')


class CartView(View):
    @staticmethod
    def get(request):
        return render(request, 'cart_page.html')

    @staticmethod
    def post(request):
        cart = json.loads(request.body.decode("utf-8"))

        response = []

        for item in cart:
            tier_id = item["tier"]
            quantity = item["quantity"]

            quantity = 20 if quantity > 20 else quantity
            quantity = 0 if quantity < 0 else quantity

            tier = get_object_or_404(ProductTier, id=tier_id)
            response.append({
                "id": tier.id,
                "name": tier.product_description.name,
                "isSingular": tier.product_description.is_singular,
                "image": tier.product_description.image,
                "tierName": tier.name,
                "price": tier.current_price,
                "quantity": quantity
            })

        return JsonResponse(response, safe=False)


class ReviewOrderView(View):
    @staticmethod
    def get(request):
        # This does not exist.
        return redirect('/cart/')

    @staticmethod
    @login_required
    def post(request):
        customer = request.user
        if not Profile.exists_for_customer(customer):
            return render(request, 'checkout.html', {
                "missing_profile": True
            })

        profile = Profile.objects.get(customer=customer)

        try:
            cart = json.loads(request.body.decode("utf-8"))
        except JSONDecodeError:
            return redirect('/cart/')

        context = validate_cart(cart)

        local_storage_cart = [{
            "tier": str(item["tier"].id),
            "quantity": item["quantity"]
        } for item in context["cart"]]

        context["local_storage_cart"] = local_storage_cart
        context["profile"] = profile

        return render(request, 'checkout.html', context)


# Validate cart, look for errors
def validate_cart(cart):
    inactive_errors = []
    out_of_stock_errors = []
    changed_quantity = []
    response_cart = []

    total_price = 0.00

    for (index, item) in enumerate(cart):
        tier_id = int(item["tier"])
        cart_quantity = int(item["quantity"])

        tiers = ProductTier.objects.filter(id=tier_id)

        if len(tiers) == 0:
            # Inexistent tier
            del cart[index]
            continue

        tier = tiers[0]

        if cart_quantity < 0:
            # No reason to keep 0 or negative quantity
            del cart[index]
            continue

        # Maximum of 20
        cart_quantity = 20 if cart_quantity > 20 else cart_quantity

        if not tier.product_description.is_active:
            # Admin discontinued product, cannot check out
            inactive_errors.append(tier)
            del cart[index]
            continue

        if tier.quantity == 0:
            # Tier is out of stock. Cannot check out
            out_of_stock_errors.append(tier)
            del cart[index]
            continue

        if tier.quantity < cart_quantity:
            # Cannot support more quantity, so quantity is changed to max possible
            cart_quantity = tier.quantity
            changed_quantity.append(tier)

        # Calculate total price
        total_price += cart_quantity * float(tier.current_price)
        response_cart.append({
            "quantity": cart_quantity,
            "tier": tier
        })

    return {
        "total_price": total_price,
        "cart": response_cart,
        "inactive_errors": inactive_errors,
        "out_of_stock_errors": out_of_stock_errors,
        "changed_quantity": changed_quantity,
    }


class FinalizeOrderView(View):
    @staticmethod
    def get(request):
        # This does not exist.
        return redirect('/cart/')

    @staticmethod
    @login_required
    def post(request):
        customer = request.user
        if not Profile.exists_for_customer(customer):
            return render(request, 'checkout.html', {
                "missing_profile": True
            })

        profile = Profile.objects.get(customer=customer)

        try:
            cart = json.loads(request.body.decode("utf-8"))
        except JSONDecodeError:
            return redirect('/cart/')

        validated_cart = validate_cart(cart)
        cart = validated_cart["cart"]
        inactive_errors = validated_cart["inactive_errors"]
        out_of_stock_errors = validated_cart["out_of_stock_errors"]
        changed_quantity = validated_cart["changed_quantity"]

        has_errors = inactive_errors or out_of_stock_errors or changed_quantity

        if has_errors:
            local_storage_cart = [{
                "tier": str(item["tier"].id),
                "quantity": item["quantity"]
            } for item in cart]

            context = validated_cart
            context["profile"] = profile
            context["local_storage_cart"] = local_storage_cart

            return render(request, 'checkout.html', context)
        else:
            order = to_order(cart, profile)
            set_order_to_expire(order)

            mail_customer_now(order)

            return render(request, 'finalized_purchase.html', {
                "order": order
            })


def to_order(cart, profile):
    order = Order.objects.create(contact=profile)

    for item in cart:
        tier = item["tier"]
        quantity = item["quantity"]

        tier.quantity -= quantity  # Deduct quantity from stock
        tier.save()

        OrderLineItem.objects.create(order=order, tier=tier, quantity=quantity)

    return order
