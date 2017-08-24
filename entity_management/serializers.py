from .models import *
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    ListField,
    IntegerField
)


class StallSerializer(ModelSerializer):
    class Meta:
        model = Stall
        fields = ('name', 'id', 'is_active')
        read_only_fields = ('id', 'is_active')


class ProductDescriptionSerializer(ModelSerializer):
    class Meta:
        model = ProductDescription
        fields = ('name', 'description', 'image', 'stall', 'id', 'is_active')
        read_only_fields = ('id', 'is_active')


class ProductTierSerializer(Serializer):
    product_description = IntegerField(min_value=0)
    tiers = ListField(child=CharField(max_length=32), min_length=1)

    def create(self, validated_data):
        for tier in validated_data.tiers:
            ProductTier.objects.create(name=tier, product_description=validated_data["product_description"])

    def update(self, instance, validated_data):
        pass

