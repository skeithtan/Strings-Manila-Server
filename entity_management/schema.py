from .models import *
from graphene_django.types import DjangoObjectType
from graphene import (
    AbstractType,
    Float,
    List,
    Field,
    Int
)


class StallType(DjangoObjectType):
    class Meta:
        model = Stall


class ProductType(DjangoObjectType):
    current_price = Float(source='current_price_history')

    class Meta:
        model = Product


class PriceHistoryType(DjangoObjectType):
    class Meta:
        model = PriceHistory


class Query(AbstractType):
    stalls = List(StallType)
    products = List(ProductType)
    stall = Field(StallType, id=Int())
    product = Field(ProductType, id=Int())

    def resolve_stall(self, args, context, info):
        id = args.get('id')
        return Stall.all_active().get(pk=id)

    def resolve_product(self, args, context, info):
        id = args.get('id')
        return Product.all_active().get(pk=id)

    def resolve_stalls(self, args, context, info):
        return Stall.all_active()

    def resolve_products(self, args, context, info):
        return Product.all_active()
