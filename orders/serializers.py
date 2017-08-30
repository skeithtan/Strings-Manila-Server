from orders.models import Order, OrderLineItem

from rest_framework.serializers import (
    ModelSerializer,
    BooleanField,
    FloatField,
    CharField,
)


class OrderLineItemSerializer(ModelSerializer):
    product = CharField(source='tier.product_description.name')
    is_singular = BooleanField(source='tier.product_description.is_singular')
    tier_name = CharField(source='tier.name')

    class Meta:
        model = OrderLineItem
        fields = ('product', 'is_singular', 'tier_name', 'tier', 'quantity')


class OrderSummarySerializer(ModelSerializer):
    total_price = FloatField()

    class Meta:
        model = Order
        fields = ('id', 'total_price', 'date_ordered', 'status')


class OrderSerializer(ModelSerializer):
    total_price = FloatField()

    class Meta:
        model = Order
        fields = '__all__'
