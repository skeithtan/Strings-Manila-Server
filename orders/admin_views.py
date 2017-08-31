from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from orders.models import Order
from admin_auth.permissions import IsSuperuser
from customer_profile.serializers import ProfileSerializer
from orders.serializers import (
    OrderSerializer,
    OrderSummarySerializer,
    OrderLineItemSerializer,
)


class OrderList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request):
        start_date = request.GET.get('start-date', None)
        end_date = request.GET.get('end-date', None)

        if start_date is None and end_date is None:
            return Response(data={
                "error": '"start-date" and "end-date" required'
            }, status=400)

        orders = Order.objects.filter(date_ordered__gte=start_date, date_ordered__lte=end_date)
        serializer = OrderSummarySerializer(orders, many=True)
        return Response(data=serializer.data, status=200)


class OrderDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_serializer = OrderSerializer(order)
        profile_serializer = ProfileSerializer(order.contact)
        order_line_item_serializer = OrderLineItemSerializer(order.orderlineitem_set.all(), many=True)

        order_data = order_serializer.data

        order_data.update({
            "profile": profile_serializer.data,
            "line_items": order_line_item_serializer.data
        })

        return Response(data=order_data, status=200)


class MarkOrderAsProcessingView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.mark_as_processing()
        return Response(status=200)


class MarkOrderAsShippedView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        store_notes = request.POST.get('notes', None)
        order.mark_as_shipped(store_notes)
        return Response(status=200)
