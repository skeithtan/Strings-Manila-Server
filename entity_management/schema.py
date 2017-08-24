from .models import *
from graphene_django.types import DjangoObjectType
from graphene import (
    AbstractType,
    Float,
    List,
    Field,
    Int
)


class ProductTierType(DjangoObjectType):
    current_price = Float(source='current_price')

    class Meta:
        model = ProductTier


class ProductDescriptionType(DjangoObjectType):
    tiers = List(ProductTierType)

    def resolve_tiers(self, args, context, info):
        return ProductDescription.objects.get(id=self.id).producttier_set.all()

    class Meta:
        model = ProductDescription


class StallType(DjangoObjectType):
    active_products = List(ProductDescriptionType)

    def resolve_active_products(self, args, context, info):
        return Stall.objects.get(id=self.id).active_products

    class Meta:
        model = Stall


class Query(AbstractType):
    stalls = List(StallType)
    products = List(ProductDescriptionType)
    stall = Field(StallType, id=Int())
    product = Field(ProductDescriptionType, id=Int())

    def resolve_stall(self, args, context, info):
        id = args.get('id')
        return Stall.all_active().get(pk=id)

    def resolve_product(self, args, context, info):
        id = args.get('id')
        return ProductDescription.all_active().get(pk=id)

    def resolve_stalls(self, args, context, info):
        return Stall.all_active()

    def resolve_products(self, args, context, info):
        return ProductDescription.all_active()
