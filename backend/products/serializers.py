from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    fk_vendor = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.FloatField()
    photo = serializers.CharField()