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
    jwt_token = request.data.get('token')
    #Autenticação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        user_id = user_json['user_id']
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)
    
    orders = Order.objects.filter(vendor_id = user_id).values()
    return Response(data=orders, status=HTTP_200_OK)

@api_view(["POST"])
def buyer_orders(request):
    jwt_token = request.data.get('token')
    #Autenticação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        user_id = user_json['user_id']
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)
    
    orders = Order.objects.filter(buyer_id = user_id).values()
    return Response(data=orders, status=HTTP_200_OK)

@api_view(["POST"])
def set_order_status(request):
    jwt_token = request.data.get('token')
    order_id = request.data.get('order_id')
    status = request.data.get('status')

    #Autenticação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        user_id = user_json['user_id']
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    if(status and order_id):
        try:
            order = Order.objects.get(id=order_id)
        except:
            return Response({'error':'Pedido não encontrado'}, status=HTTP_404_NOT_FOUND)
   
        if(order.buyer_id !=  user_id or order.vendor_id !=  user_id):
            return Response({'error':'Permissão negada'}, status=HTTP_403_FORBIDDEN)

        if(status == 'open' or status == 'closed'):
            order.status = status
            order.save()
            serializer = OrderSerializer(order)
            return Response(data=serializer.data,status=HTTP_200_OK)
        else:
            return Response({'error':'Status inválido'}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)
    return

