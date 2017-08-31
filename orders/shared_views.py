from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from orders.models import Order


class CancelOrderView(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if order.status == 'S':
            # Cannot cancel a Shipped order. Not even admins can do that.
            return Response(status=400)

        user = request.user

        # Administrator can cancel whatever he wants
        if user.is_superuser:
            order.cancel()
            return Response(status=200)

        # Only admins can cancel orders that aren't Unpaid
        if order.status != 'U':
            return Response(status=403)

        # Customers can only cancel their own orders
        if order.contact.customer == user:
            order.cancel()
            return redirect(f"/orders/{order.id}/")

        return Response(status=403)
