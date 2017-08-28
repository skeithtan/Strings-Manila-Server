import json

from django.views import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from entity_management.models import ProductTier
from waitlists.models import Waitlist


class ProductCatalogView(View):
    @staticmethod
    def get(request):
        user = request.user

        waitlists_for_user = [] if not user.is_authenticated else Waitlist.objects.filter(customer=user)
        waitlist_tier_id = [waitlist.tier.id for waitlist in waitlists_for_user]

        return render(request, 'products_catalog.html', {
            "waitlisted": waitlist_tier_id
        })


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
