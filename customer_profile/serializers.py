from .models import Profile
from rest_framework.serializers import ModelSerializer, CharField


class ProfileSerializer(ModelSerializer):
    customer_name = CharField(source='customer.get_full_name', read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('customer', )
