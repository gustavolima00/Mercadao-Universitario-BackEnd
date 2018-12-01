from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR
)
import requests
import jwt
from backend.settings_secret import *

@api_view(["POST"])
def create_product(request):

    return

@api_view(["POST"])
def delete_product(request):

    return

@api_view(["POST"])
def edit_product(request):

    return

@api_view(["POST"])
def get_product(request):

    return

@api_view(["GET"])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products)
    return Response(data=serializer.data,status=HTTP_200_OK)
