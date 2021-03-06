from datetime import timedelta

from customer_profile.models import Profile
from entity_management.models import ProductTier
from recommendations.models import ProductOccurrence, ProductPairOccurrence

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

    @property
    def expiration_date(self):
        return self.date_ordered + timedelta(days=3)

    def mark_as_shipped(self, store_notes):
        self.status = 'S'
        self.store_notes = store_notes
        self.mark_occurrence()
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

        for line_item in self.orderlineitem_set.all():
            line_item.tier.quantity += line_item.quantity
            line_item.tier.save()

        self.save()

    def mark_occurrence(self):
        line_items = self.orderlineitem_set.all()

        for line_item in line_items:
            ProductOccurrence.increment_for_product(line_item.tier.product_description)

        # Create Combination Permutation List
        for index, line_item in enumerate(line_items):
            product_1 = line_item.tier.product_description

            # + 1 because you shouldn't count self. Indexes start with 0.
            for line_item_2 in line_items[index + 1:]:
                product_2 = line_item_2.tier.product_description

                ProductPairOccurrence.increment_for_pair(product_1, product_2)

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
