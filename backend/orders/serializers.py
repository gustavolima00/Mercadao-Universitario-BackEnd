from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    created = serializers.DateTimeField()
    vendor_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField()
    vendor_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    status = serializers.TextField()