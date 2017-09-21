from collections import namedtuple

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from entity_management.models import Collection, ProductDescription
from orders.models import Order
from admin_auth.permissions import IsSuperuser
from customer_profile.serializers import ProfileSerializer
from orders.serializers import (
    OrderSerializer,
    OrderSummarySerializer,
    OrderLineItemSerializer,
)

from .tasks import mail_customer_now


class OrderList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request):
        start_date = request.GET.get('start-date', None)
        end_date = request.GET.get('end-date', None)

        if start_date is None and end_date is None:
            return Response(data={
                "error": '"start-date" and "end-date" required'
            }, status=400)

        orders = Order.objects.filter(date_ordered__gte=start_date, date_ordered__lte=end_date)
        serializer = OrderSummarySerializer(orders, many=True)
        return Response(data=serializer.data, status=200)


class OrderDetail(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_serializer = OrderSerializer(order)
        profile_serializer = ProfileSerializer(order.contact)
        order_line_item_serializer = OrderLineItemSerializer(order.orderlineitem_set.all(), many=True)

        order_data = order_serializer.data

        order_data.update({
            "profile": profile_serializer.data,
            "line_items": order_line_item_serializer.data
        })

        return Response(data=order_data, status=200)


class MarkOrderAsProcessingView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.mark_as_processing()

        mail_customer_now(order)

        return Response(status=200)


class MarkOrderAsShippedView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def post(request, order_id):
        order = get_object_or_404(Order, id=order_id)
        store_notes = request.POST.get('notes', None)
        order.mark_as_shipped(store_notes)

        mail_customer_now(order)

        return Response(status=200)


class SalesGenerator:
    def __init__(self, orders):
        line_items = []
        for order in orders:
            line_items += order.orderlineitem_set.all()

        self.line_items = line_items

    def get_sales(self):
        collections = Collection.objects.filter(is_active=True)

        sales_per_collection = []
        total_sales = 0
        total_quantity = 0

        for collection in collections:
            collection_sales = self.get_collection_sales(collection)

            sales_per_collection.append({
                "id": collection.id,
                "name": collection.name,
                "sales": collection_sales.sales,
                "quantity": collection_sales.quantity,
                "product_sales": collection_sales.sales_per_product
            })

            total_sales += collection_sales.sales
            total_quantity += collection_sales.quantity

        return {
            "total_sales": total_sales,
            "total_quantity": total_quantity,
            "collection_sales": sales_per_collection
        }

    def get_collection_sales(self, collection):
        products = collection.productdescription_set.filter(is_active=True)

        sales_per_product = []
        total_collection_sales = 0
        total_collection_quantity = 0

        for product in products:
            product_sales = self.get_product_sales(product)
            sales_per_product.append({
                "id": product.id,
                "name": product.name,
                "is_singular": product.is_singular,
                "quantity": product_sales.quantity,
                "sales": product_sales.sales,
                "tier_sales": product_sales.tier_sales
            })

            total_collection_sales += product_sales.sales
            total_collection_quantity += product_sales.quantity

        CollectionSales = namedtuple('CollectionSales', ['sales_per_product', 'quantity', 'sales'])
        return CollectionSales(sales_per_product=sales_per_product, quantity=total_collection_quantity, sales=total_collection_sales)

    def get_product_sales(self, product):
        tiers = product.producttier_set.all()

        tier_sales_dict = {}
        total_product_quantity = 0
        total_product_sales = 0

        for tier in tiers:
            tier_sales_dict[tier.id] = {
                "name": tier.name,
                "quantity": 0,
                "sales": 0
            }

        for line_item in self.line_items:
            if line_item.tier in tiers:
                tier = line_item.tier
                line_price = line_item.line_price
                line_quantity = line_item.quantity

                tier_sales_dict[tier.id]["sales"] += line_price
                tier_sales_dict[tier.id]["quantity"] += line_quantity

                total_product_quantity += line_quantity
                total_product_sales += line_price

        tier_sales = []

        for tier_id, sales in tier_sales_dict.items():
            tier_sale = sales
            tier_sale["id"] = tier_id
            tier_sales.append(tier_sale)

        ProductSales = namedtuple('ProductSales', ['tier_sales', 'quantity', 'sales'])
        return ProductSales(tier_sales=tier_sales, quantity=total_product_quantity, sales=total_product_sales)


class SalesView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperuser)

    @staticmethod
    def get(request):
        start_date = request.GET.get('start-date', None)
        end_date = request.GET.get('end-date', None)

        if start_date is None and end_date is None:
            return Response(data={
                "error": '"start-date" and "end-date" required'
            }, status=400)

        orders = Order.objects.filter(date_ordered__gte=start_date, date_ordered__lte=end_date, status='S')
        sales = SalesGenerator(orders).get_sales()
        return Response(data=sales, status=200)

