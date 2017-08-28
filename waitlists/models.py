from entity_management.models import ProductTier

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models import (
    Model,
    DateTimeField,
    ForeignKey
)


class Waitlist(Model):
    customer = ForeignKey(User)
    tier = ForeignKey(ProductTier)
    date = DateTimeField(auto_now=True)

    def __str__(self):
        tier_name = "N/A" if self.tier.product_description.is_singular else self.tier.name
        return f"{self.tier.product_description.name} - {tier_name} - {self.customer.get_full_name()}"


@receiver(post_save, sender=Waitlist)
def on_waitlist_save(sender, instance, created, **kwargs):
    if not created:
        return

    instance.tier.increment_waitlist()
