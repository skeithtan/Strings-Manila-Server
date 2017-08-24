from datetime import datetime
from django.db.models import (
    Model,
    CharField,
    DecimalField,
    ForeignKey,
    PositiveIntegerField,
    CASCADE,
    BooleanField,
    DateTimeField
)


class Stall(Model):
    name = CharField(max_length=64)
    is_active = BooleanField(default=True)

    @staticmethod
    def all_active():
        return Stall.objects.filter(is_active=True)

    @property
    def active_products(self):
        return self.productdescription_set.filter(is_active=True)

    def deactivate(self):
        self.is_active = False
        for product in self.productdescription_set.all():
            product.deactivate()

        self.save()

    def __str__(self):
        return self.name if self.is_active else f"DEACTIVATED - {self.name}"


class ProductDescription(Model):
    name = CharField(max_length=64)
    description = CharField(max_length=256)
    image = CharField(max_length=256, default="http://i.imgur.com/a0HmrDW.png")
    stall = ForeignKey(Stall, on_delete=CASCADE)
    is_active = BooleanField(default=True)

    @staticmethod
    def all_active():
        return ProductDescription.objects.filter(is_active=True)

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            self.save()

    def __str__(self):
        return f"{self.name}" if self.is_active else f"DEACTIVATED - {self.name}"


class ProductTier(Model):
    name = CharField(max_length=32)
    product_description = ForeignKey(ProductDescription, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)

    @property
    def current_price_history(self):
        return self.pricehistory_set.all().order_by('-effective_from')[0]

    @property
    def current_price(self):
        return self.current_price_history.price

    def change_price(self, new_price):
        current_price_history = self.current_price_history
        current_price_history.effective_to = datetime.now()
        current_price_history.save()
        self.pricehistory_set.create(price=new_price)

    def price_for_date(self, date):
        # Cut off all that are not within parameter date range and sort descending (present to past)
        price_histories = self.pricehistory_set.filter(effective_from__lte=date).order_by("-effective_from")
        # Take most recent entry
        return price_histories[0].price


class PriceHistory(Model):
    product_tier = ForeignKey(ProductTier, on_delete=CASCADE)
    price = DecimalField(decimal_places=2, max_digits=10)
    effective_from = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.price} - {self.effective_from}"
