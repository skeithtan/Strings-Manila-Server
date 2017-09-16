from django.db.models import Model, CharField


class BankDepositAccount(Model):
    bank_name = CharField(max_length=32)
    account_holder_name = CharField(max_length=32)
    account_number = CharField(max_length=32)
