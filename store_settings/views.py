import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from admin_auth.permissions import IsSuperuser

from store_settings.user_settings import StoreStatus


class SettingsOverview(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request):
        overview = {
            "on_maintenance": StoreStatus.on_maintenance,
            "current_user": request.user.get_full_name()
        }
        return Response(data=json.dumps(overview), status=200)


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
        StoreStatus.disable_maintenance()
        return Response(200)
