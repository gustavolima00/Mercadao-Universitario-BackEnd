from rest_framework import serializers
from .models import Product
from profiles.serializers import ProfileSerializer

class ProductSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    created = serializers.DateTimeField()
    vendor = ProfileSerializer()
    name = serializers.CharField()
    price = serializers.FloatField()
    photo = serializers.CharField()