from customer_profile.models import Profile
from entity_management.models import ProductTier

from django.db.models import (
    Model,
    CASCADE,
    CharField,
    ForeignKey,
    DateTimeField,
    PositiveIntegerField,
)


class Order(Model):
    ORDER_STATUSES = (
        ('U', 'Unpaid'),
        ('V', 'Verifying Payment'),
        ('P', 'Processing'),
        ('S', 'Shipped'),
        ('C', 'Cancelled')
    )

    date_ordered = DateTimeField(auto_now=True)
    contact = ForeignKey(Profile, on_delete=CASCADE)
    status = CharField(max_length=2, choices=ORDER_STATUSES, default='U')
    deposit_photo = CharField(max_length=256, null=True, default=None)

    @property
    def total_price(self):
        order_items = self.orderlineitem_set.all()
        total_price = 0.00
        for order_item in order_items:
            total_price += float(order_item.line_price)
        return total_price


class OrderLineItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE)
    tier = ForeignKey(ProductTier, on_delete=CASCADE)
    quantity = PositiveIntegerField()

    @property
    def line_price(self):
        date_ordered = self.order.date_ordered
        price = self.tier.price_for_date(date=date_ordered)
        return float(price) * float(self.quantity)
