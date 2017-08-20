from .models import *
from rest_framework.serializers import ModelSerializer


class StallSerializer(ModelSerializer):
    class Meta:
        model = Stall
        fields = ('name', 'id', 'is_active')
        read_only_fields = ('id', 'is_active')


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'stall', 'id', 'is_active')
        read_only_fields = ('id', 'is_active')
