from django.contrib.auth.models import User
from django.db.models import (
    Model,
    OneToOneField,
    CharField,
    EmailField,
)


class Profile(Model):
    customer = OneToOneField(User)
    email = EmailField()
    phone = CharField(max_length=32)
    city = CharField(max_length=64)
    address = CharField(max_length=1024)
    postal_code = CharField(max_length=32)

    @staticmethod
    def exists_for_customer(customer):
        return Profile.objects.filter(customer=customer).count() >= 1

    def __str__(self):
        return self.customer.get_full_name()
