from rest_framework.serializers import ModelSerializer

from orders.models import Order, OrderLineItem


class OrderLineItemSerializer(ModelSerializer):
    class Meta:
        model = OrderLineItem
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
