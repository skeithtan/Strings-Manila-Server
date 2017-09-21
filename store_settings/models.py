from solo.models import SingletonModel
from django.db.models import (
    Model,
    CharField,
    BooleanField,
    DecimalField,
)


class SiteConfiguration(SingletonModel):
    metro_manila = DecimalField(decimal_places=2, max_digits=10, default=0)
    province = DecimalField(decimal_places=2, max_digits=10, default=0)
    maintenance_mode = BooleanField(default=True)


class BankDepositAccount(Model):
    bank_name = CharField(max_length=32)
    account_holder_name = CharField(max_length=32)
    account_number = CharField(max_length=32)
