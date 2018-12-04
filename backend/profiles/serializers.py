from django.contrib.auth.models import User
from .models import Profile
from .models import Location
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField()
    username = serializers.CharField(max_length=200)

class LocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

class ProfileSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    user = UserSerializer()
    name = serializers.CharField(max_length=30)
    photo = serializers.CharField()
    profile_type = serializers.IntegerField()
    location = LocationSerializer()