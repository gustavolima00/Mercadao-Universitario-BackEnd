from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
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
def create_order(request):
    return

@api_view(["POST"])
def vendor_orders(request):
    return

@api_view(["POST"])
def buyer_orders(request):
    return

@api_view(["POST"])
def set_order_status(request):
    return

