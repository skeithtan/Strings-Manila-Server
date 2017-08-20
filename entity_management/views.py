from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from .serializers import *
from admin_auth.permissions import IsSuperuser


class StallList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request):
        serializer = StallSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)
        else:
            return Response(serializer.errors, 400)

        return Response(status=200)


class StallDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def put(request, stall_id):
        serializer = StallSerializer(data=request.data)

        if serializer.is_valid():
            stall = get_object_or_404(Stall, id=stall_id)
            stall.name = serializer.validated_data["name"]
            stall.save()
        else:
            return Response(serializer.errors, 400)

        return Response(status=200)

    @staticmethod
    def delete(request, stall_id):
        stall = get_object_or_404(Stall, id=stall_id)
        stall.deactivate()
        return Response(status=200)


class ProductList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, stall_id):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(serializer.validated_data)
        else:
            return Response(serializer.errors, 400)

        return Response(status=200)


class ProductDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def put(request, product_id):
        pass

    @staticmethod
    def delete(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.deactivate()
        return Response(status=200)