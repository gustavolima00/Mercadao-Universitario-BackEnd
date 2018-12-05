from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from profiles.models import (
    Profile,
    VENDOR_NOT_APPROVED,
    VENDOR_APPROVED,
    BUYER,
)
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
import geopy.distance

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
        if(profile.profile_type == BUYER):
            return Response({'error':'Usuário não autorizado'}, status=HTTP_403_FORBIDDEN)

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
    vendors = Profile.objects.filter(profile_type = VENDOR_APPROVED)
    products = Product.objects.filter(vendor__in = vendors)
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data,status=HTTP_200_OK)

@api_view(["POST"])
def nearby_products(request):
    #Requests
    latitude1 = request.data.get('latitude')
    longitude1 = request.data.get('longitude')
    min_distance = request.data.get('distance')

    if(latitude1 and longitude1 and min_distance):
        profiles = []
        for profile in Profile.objects.filter(profile_type = VENDOR_APPROVED):
            if(profile.location.latitude and profile.location.longitude):
                latitude2=float(profile.location.latitude)
                longitude2=float(profile.location.longitude)
                coords_1 = (latitude1, longitude1)
                coords_2 = (latitude2, longitude2)
                distance = geopy.distance.vincenty(coords_1, coords_2).m
                if(distance<float(min_distance)):
                    profiles.append(profile)
                print('distance', distance)
    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

    print(profiles)
    products = Product.objects.filter(vendor__in = profiles)
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data,status=HTTP_200_OK)

@api_view(["POST"])
def search_products(request):
    name = request.data.get('name')

    vendors = Profile.objects.filter(profile_type = VENDOR_APPROVED)
    all_products = Product.objects.filter(vendor__in = vendors)
    products = all_products.filter(name__contains=name)
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data,status=HTTP_200_OK)