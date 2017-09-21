from .models import Collection, ProductDescription, ProductTier
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    FloatField,
    IntegerField
)


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = ('name', 'id', 'is_active')
        read_only_fields = ('id', 'is_active')


class ProductTierSerializer(Serializer):
    id = IntegerField(min_value=0, required=False)
    name = CharField(max_length=32)
    price = FloatField(min_value=0)
    product_description = None

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ProductSerializer(Serializer):
    name = CharField(max_length=64)
    description = CharField(max_length=256)
    image = CharField(max_length=256, required=False)
    tiers = ProductTierSerializer(many=True)
    collection = None

    def create(self, validated_data):
        if "image" in validated_data:
            product_description = ProductDescription.objects.create(name=validated_data["name"],
                                                                    description=validated_data["description"],
                                                                    image=validated_data["image"],
                                                                    collection=self.collection)
        else:
            product_description = ProductDescription.objects.create(name=validated_data["name"],
                                                                    description=validated_data["description"],
                                                                    collection=self.collection)

        for tier in validated_data["tiers"]:
            product_tier = ProductTier.objects.create(name=tier["name"],
                                                      product_description=product_description)

            product_tier.set_price(tier["price"])

        return product_description

    def update(self, instance, validated_data):
        if "image" in validated_data:
            instance.image = validated_data["image"]

        instance.name = validated_data["name"]
        instance.description = validated_data["description"]

        for validated_data_tier in validated_data["tiers"]:
            print(validated_data_tier)
            tier = ProductTier.objects.get(id=validated_data_tier["id"])
            tier.name = validated_data_tier["name"]

            if tier.current_price != validated_data_tier["price"]:
                tier.set_price(validated_data_tier["price"])

            tier.save()

        instance.save()
