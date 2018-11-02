from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
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
def create_profile(request):
    #Requests
    jwt_token = request.data.get('jwt_token')
    name = request.data.get('name')
    photo_data = request.data.get('photo')

    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        print(user_json)
        user = User.objects.get(username = user_json['username'])
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    if(name and photo_data):
        photo = cloudinary.uploader.upload(photo_data)
        photo_url = photo['url']
        profile = Profile(user=user, name=name, photo=photo_url)

    else:
        return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

    return Response(status=HTTP_200_OK)
