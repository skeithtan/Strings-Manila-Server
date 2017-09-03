from recommendations.models import Recommendation
from .models import Stall, ProductDescription, ProductTier

from graphene_django.types import DjangoObjectType
from graphene import (
    AbstractType,
    Boolean,
    Float,
    List,
    Field,
    Int
)


class ProductTierType(DjangoObjectType):
    current_price = Float(source='current_price')

    class Meta:
        model = ProductTier
        exclude_fields = ('orderlineitem_set', )


class ProductDescriptionType(DjangoObjectType):
    tiers = List(ProductTierType)
    is_singular = Boolean(source='is_singular')
    recommendations = List(Int)

    def resolve_tiers(self, args, context, info):
        return ProductDescription.objects.get(id=self.id).producttier_set.all()

    def resolve_recommendations(self, args, context, info):
        root_product = ProductDescription.objects.get(id=self.id)
        return [product.id for product in Recommendation.recommendation_for_product(root_product)]

    class Meta:
        model = ProductDescription


class StallType(DjangoObjectType):
    active_products = List(ProductDescriptionType)

    def resolve_active_products(self, args, context, info):
        return Stall.objects.get(id=self.id).active_products

    class Meta:
        model = Stall


class Query(AbstractType):
    # Plural
    stalls = List(StallType)
    products = List(ProductDescriptionType)
    tiers = List(ProductTierType)
    # Singular
    stall = Field(StallType, id=Int())
    product = Field(ProductDescriptionType, id=Int())
    tier = Field(ProductTierType, id=Int())

    def resolve_stall(self, args, context, info):
        return Stall.all_active().get(pk=args.get('id'))

    def resolve_product(self, args, context, info):
        return ProductDescription.all_active().get(pk=args.get('id'))

    def resolve_tier(self, args, context, info):
        return ProductTier.objects.get(pk=args.get('id'))

    def resolve_stalls(self, args, context, info):
        return Stall.all_active()

    def resolve_products(self, args, context, info):
        return ProductDescription.all_active()

    def resolve_tiers(self, args, context, info):
        return ProductTier.objects.all().filter(product_description__is_active=True)
