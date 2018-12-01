from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    created = serializers.DateTimeField()
    vendor_id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()
    photo = serializers.CharField()