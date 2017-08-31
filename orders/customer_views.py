from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from orders.models import Order
from customer_profile.models import Profile


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
