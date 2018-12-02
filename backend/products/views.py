from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from profiles.models import Profile
from django.contrib.auth.models import User
from .serializers import ProductSerializer
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
import jwt
from backend.settings_secret import *

DEFAULT_PHOTO = 'https://ecservice.rakuten.com.br/rux/wp-content/themes/RUX/images/no-photo.png'

@api_view(["POST"])
def create_product(request):
    jwt_token = request.data.get('token')
    name = request.data.get('name')
    price = request.data.get('price')
    photo_data = request.data.get('photo')

    #Autenticação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        username = user_json['username']
        user = User.objects.get(username = username)
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    try:
        profile = Profile.objects.get(user=user)

    except Profile.DoesNotExist:
        return Response({'error':'Usuário não possui perfil'}, status=HTTP_403_FORBIDDEN)

    if(name and price):
        if(photo_data):
            photo = cloudinary.uploader.upload(photo_data)
            photo_url = photo['url']
        else:
            photo_url = DEFAULT_PHOTO

        try:
            product = Product(vendor=profile, name=name, price=price, photo=photo_url)
            product.save()
        except:
            return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

    serializer = ProductSerializer(product)
    return Response(data=serializer.data,status=HTTP_200_OK)

@api_view(["POST"])
def delete_product(request):
    jwt_token = request.data.get('token')
    product_id = request.data.get('product_id')

    #Autenticação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        username = user_json['username']
        user = User.objects.get(username = username)
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    try:
        profile = Profile.objects.get(user=user)

    except Profile.DoesNotExist:
        return Response({'error':'Usuário não possui perfil'}, status=HTTP_403_FORBIDDEN)

    if(product_id):
        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response({'error':'Produto não encontrado'}, status=HTTP_404_NOT_FOUND)
        if (product.vendor == profile):
            product.delete()
            return Response({'sucess':'O produto foi deletado com sucesso'}, status=HTTP_200_OK )
        else:
            return Response({'error':'O produto não pertence ao usuário'}, status=HTTP_403_FORBIDDEN)
    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def edit_product(request):
    jwt_token = request.data.get('token')
    product_id = request.data.get('product_id')
    name = request.data.get('name')
    price = request.data.get('price')
    photo_data = request.data.get('photo')

    #Autenticação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        username = user_json['username']
        user = User.objects.get(username = username)
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    try:
        profile = Profile.objects.get(user=user)

    except Profile.DoesNotExist:
        return Response({'error':'Usuário não possui perfil'}, status=HTTP_403_FORBIDDEN)

    if(product_id):
        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response({'error':'Produto não encontrado'}, status=HTTP_404_NOT_FOUND)
        if (product.vendor == profile):
            if(price):
                try:
                    product.price = price
                    product.save()
                except:
                    return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

            if(name):
                product.name = name
                product.save()

            if(photo_data):
                photo = cloudinary.uploader.upload(photo_data)
                photo_url = photo['url']
                product.photo = photo_url
                product.save()
        else:
            return Response({'error':'O produto não pertence ao usuário'}, status=HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(product)
        return Response(data=serializer.data,status=HTTP_200_OK)
    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def get_product(request):
    product_id = request.data.get('product_id')
    if(product_id):
        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response({'error':'Produto não encontrado'}, status=HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(data=serializer.data,status=HTTP_200_OK)
    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_products(request):
    jwt_token = request.data.get('token')

    #Autenticação do usuário
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        username = user_json['username']
        user = User.objects.get(username = username)
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    try:
        profile = Profile.objects.get(user=user)

    except Profile.DoesNotExist:
        return Response({'error':'Usuário não possui perfil'}, status=HTTP_403_FORBIDDEN)

    products = Product.objects.filter(vendor = profile)
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data,status=HTTP_200_OK)
    
@api_view(["GET"])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data,status=HTTP_200_OK)
