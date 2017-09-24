from rest_framework.serializers import ModelSerializer

from .models import *


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        exclude = ('is_active', )


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        exclude = ('is_active', )


class MaterialSerializer(ModelSerializer):
    class Meta:
        model = Material
        exclude = ('is_active', )


class MaterialTypeSerializer(ModelSerializer):
    class Meta:
        model = MaterialType
        exclude = ('is_active', )
