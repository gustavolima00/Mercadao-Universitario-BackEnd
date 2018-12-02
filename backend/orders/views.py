from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from products.models import Product
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
    jwt_token = request.data.get('token')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    #Autenticação e verificação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        user_id = user_json['user_id']
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    if(product_id and quantity):
        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response({'error':'Produto não encontrado'}, status=HTTP_404_NOT_FOUND)
        try:
            order = Order(vendor_id=product.vendor_id, buyer_id=user_id, product_id= product.id, quantity=quantity)
            order.save()
        except:
            return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order)
        return Response(data=serializer.data,status=HTTP_200_OK)
    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def vendor_orders(request):
    return

@api_view(["POST"])
def buyer_orders(request):
    return

@api_view(["POST"])
def set_order_status(request):
    return

