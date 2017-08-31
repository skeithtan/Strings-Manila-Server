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

    date_ordered = DateTimeField(auto_now_add=True)
    contact = ForeignKey(Profile, on_delete=CASCADE)
    status = CharField(max_length=2, choices=ORDER_STATUSES, default='U')
    deposit_photo = CharField(max_length=256, null=True, default=None)
    store_notes = CharField(max_length=1024, null=True, default=None)

    @property
    def total_price(self):
        order_items = self.orderlineitem_set.all()
        total_price = 0.00
        for order_item in order_items:
            total_price += float(order_item.line_price)
        return total_price

    def mark_as_shipped(self, store_notes):
        self.status = 'S'
        self.store_notes = store_notes
        self.save()

    def mark_as_processing(self):
        self.status = 'P'
        self.save()

    def set_payment(self, deposit_photo_link):
        self.deposit_photo = deposit_photo_link
        self.status = 'V'
        self.save()

    def cancel(self):
        self.status = 'C'
        self.save()

    def __str__(self):
        return f"Order {self.id} / {self.date_ordered} / {self.contact}"


class OrderLineItem(Model):
    order = ForeignKey(Order, on_delete=CASCADE)
    tier = ForeignKey(ProductTier, on_delete=CASCADE)
    quantity = PositiveIntegerField()

    @property
    def line_price(self):
        date_ordered = self.order.date_ordered
        price = self.tier.price_for_date(date=date_ordered)
        return float(price) * float(self.quantity)

    @property
    def unit_price(self):
        # Price at the time object was created
        date_ordered = self.order.date_ordered
        return self.tier.price_for_date(date=date_ordered)

    def __str__(self):
        return f"Order {self.order.id} - {self.tier.name} - {self.quantity}"
