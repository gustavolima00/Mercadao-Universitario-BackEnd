from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=200)


class ProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    name = serializers.CharField(max_length=30)
    photo = serializers.CharField()
    seller = serializers.BooleanField()