from django.contrib.auth.models import User
from django.db.models import (
    Model,
    OneToOneField,
    CharField,
    EmailField
)


class Profile(Model):
    customer = OneToOneField(User)
    email = EmailField()
    phone = CharField(max_length=32)
    city = CharField(max_length=64)
    address = CharField(max_length=1024)
    postal_code = CharField(max_length=32)
