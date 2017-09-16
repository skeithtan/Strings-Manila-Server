from .models import BankDepositAccount
from rest_framework.serializers import ModelSerializer


class BankDepositAccountSerializer(ModelSerializer):
    class Meta:
        model = BankDepositAccount
        fields = '__all__'
