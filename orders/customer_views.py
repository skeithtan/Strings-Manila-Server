from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.views import APIView
from rest_framework.response import Response

from orders.models import Order
from customer_profile.models import Profile
from store_settings.models import BankDepositAccount


class OrdersView(View):
    @staticmethod
    @login_required
    def get(request):
        user = request.user

        if not Profile.exists_for_customer(user):
            # You can't have an order without a profile.
            return render(request, 'orders.html', {
                "orders": []
            })

        profile = Profile.objects.get(customer=user)
        order_list = Order.objects.filter(contact=profile).order_by('-date_ordered')  # Most recent first

        paginator = Paginator(order_list, 15)
        page = request.GET.get('page', 1)

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            orders = paginator.page(1)
        except EmptyPage:
            # If page is not an integer, deliver first page.
            orders = paginator.page(paginator.num_pages)

        return render(request, 'orders.html', {
            "orders": orders
        })


class OrderDetailView(View):
    @staticmethod
    @login_required
    def get(request, order_id):
        user = request.user

        if not Profile.exists_for_customer(user):
            # You can't have an order without a profile.
            return redirect('/orders/')

        profile = Profile.objects.get(customer=user)
        orders = Order.objects.filter(contact=profile)
        orders = orders.filter(id=order_id)

        if not orders:
            # Either it's not the user's order or the order doesn't exist.
            # Either way, show them the proverbial door.
            return redirect('/orders/')

        order = orders[0]
        return render(request, 'order_detail.html', {
            "order": order,
            "accounts": BankDepositAccount.objects.all()
        })


class SubmitPaymentView(APIView):
    @staticmethod
    @login_required
    def post(request, order_id):
        user = request.user

        if not Profile.exists_for_customer(user):
            # You can't have an order without a profile.
            return redirect('/orders/')

        profile = Profile.objects.get(customer=user)
        orders = Order.objects.filter(contact=profile)
        orders = orders.filter(id=order_id)

        if not orders:
            # You can't pay for someone else's order. Hmm.... good feature?
            return redirect('/orders/')

        deposit_photo_link = request.POST.get('image', None)

        if not deposit_photo_link:
            return Response(data={"error": "image required"}, status=400)

        order = orders[0]
        order.set_payment(deposit_photo_link)

        return Response(status=200)
