import json

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
            return Response(status=200)
        else:
            return Response(serializer.errors, 400)


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
            return Response(status=200)
        else:
            return Response(serializer.errors, 400)

    @staticmethod
    def delete(request, stall_id):
        stall = get_object_or_404(Stall, id=stall_id)
        stall.discontinue()
        return Response(status=200)


class ProductList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, stall_id):
        stall = get_object_or_404(Stall, id=stall_id)
        product_serializer = ProductSerializer(data=json.loads(request.body.decode("utf-8")))
        product_serializer.stall = stall

        if product_serializer.is_valid():
            product_serializer.create(product_serializer.validated_data)
            return Response(status=200)

        else:
            return Response(product_serializer.errors, 400)


class ProductDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def patch(request, product_id):
        product_description = get_object_or_404(ProductDescription, id=product_id)
        serializer = ProductSerializer(data=json.loads(request.body.decode("utf-8")), partial=True)

        if serializer.is_valid():
            serializer.update(instance=product_description, validated_data=serializer.validated_data)
            return Response(status=200)
        else:
            return Response(serializer.errors, 400)

    @staticmethod
    def delete(request, product_id):
        product = get_object_or_404(ProductDescription, id=product_id)
        product.discontinue()
        return Response(status=200)


class RestockTierView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, tier_id):
        product_tier = get_object_or_404(ProductTier, id=tier_id)

        if "quantity" not in request.data or "add" not in request.data:
            return Response({
                "error": '"quantity" and "add" required'
            }, status=400)

        quantity = request.data["quantity"]
        is_add = request.data["add"]

        if is_add == "true":
            is_add = True
        elif is_add == "false":
            is_add = False
        else:
            return Response({
                "error": '"add" must be true or false'
            }, status=400)

        try:
            quantity = int(quantity)
        except:
            return Response({
                "error": '"quantity" must be an integer'
            }, status=400)

        if quantity < 0:
            return Response({
                "error": '"quantity" must be greater than 0'
            }, status=400)

        if is_add:
            product_tier.quantity += quantity
        else:
            if quantity >= product_tier.quantity:
                product_tier.quantity = 0
            else:
                product_tier.quantity -= quantity

        product_tier.save()
        return Response(status=200)
