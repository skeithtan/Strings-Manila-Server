import json

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from admin_auth.permissions import IsSuperuser

from store_settings.user_settings import StoreStatus
from store_settings.models import BankDepositAccount
from store_settings.serializers import BankDepositAccountSerializer


class SettingsOverview(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request):

        bank_accounts = BankDepositAccount.objects.all()
        bank_account_serializer = BankDepositAccountSerializer(bank_accounts, many=True)

        overview = {
            "on_maintenance": StoreStatus.on_maintenance,
            "accounts": bank_account_serializer.data,
            "current_user": request.user.get_full_name()
        }
        return Response(data=overview, status=200)


class EnableMaintenanceMode(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request):
        StoreStatus.enable_maintenance()
        return Response(200)


class DisableMaintenanceMode(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request):
        if BankDepositAccount.objects.all().count() == 0:
            return Response(data={
                "error": "Cannot take out of maintenance mode when there are no bank accounts."
            }, status=400)

        StoreStatus.disable_maintenance()
        return Response(200)


class BankAccountList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request):
        serializer = BankDepositAccountSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(status=200)
        else:
            return Response(serializer.errors, 400)


class BankAccountDetail(APIView):
    @staticmethod
    def put(request, bank_account_id):
        account = get_object_or_404(BankDepositAccount, id=bank_account_id)
        serializer = BankDepositAccountSerializer(data=request.data)

        if serializer.is_valid():
            new_data = serializer.validated_data
            account.bank_name = new_data["bank_name"]
            account.account_holder_name = new_data["account_holder_name"]
            account.account_number = new_data["account_number"]
            account.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, 400)

    @staticmethod
    def delete(request, bank_account_id):
        account = get_object_or_404(BankDepositAccount, id=bank_account_id)
        account.delete()

        # Cannot sell items if the customers cannot pay.
        if BankDepositAccount.objects.all().count() == 0:
            StoreStatus.enable_maintenance()

        return Response(status=200)
