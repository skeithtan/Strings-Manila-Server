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
        stall.deactivate()
        return Response(status=200)


class ProductList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, stall_id):
        request_data = request.data.copy()
        request_data["stall"] = stall_id
        serializer = ProductSerializer(data=request_data)

        if "price" not in request_data:
            return Response({
                "error": "Price required"
            }, 400)

        if serializer.is_valid():
            product = serializer.create(serializer.validated_data)
            PriceHistory.objects.create(product=product, price=request_data["price"])
            return Response(status=200)
        else:
            return Response(serializer.errors, 400)


class ProductDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def patch(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)

        if "price" not in request.data:
            return Response({
                "error": "Price required"
            }, 400)

        request_product_price = request.data["price"]

        if request_product_price != product.current_price:
            PriceHistory.objects.create(product=product, price=request_product_price)

        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        else:
            return Response(serializer.errors, 400)

    @staticmethod
    def delete(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.deactivate()
        return Response(status=200)
