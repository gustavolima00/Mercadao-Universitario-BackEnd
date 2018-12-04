from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .models import Location
from .serializers import ProfileSerializer
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from .models import (
    VENDOR_NOT_APPROVED,
    VENDOR_APPROVED,
    BUYER,
)
import requests
import jwt
from backend.settings_secret import *

DEFAULT_PHOTO = 'https://i.imgur.com/UWQ0GOq.png'

@api_view(["GET"])
def all_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(data=serializer.data,status=HTTP_200_OK)

@api_view(["POST"])
def create_profile(request):
    #Requests
    jwt_token = request.data.get('token')
    name = request.data.get('name')
    photo_data = request.data.get('photo')
    profile_type = request.data.get('profile_type')
    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        username = user_json['username']
        user = User.objects.get(username = username)
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    try:
        profile = Profile.objects.get(user=user)
        return Response({'error':'Usuário já possui perfil'}, status=HTTP_400_BAD_REQUEST)

    except Profile.DoesNotExist:
        if(not name or not profile_type):
            return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

        profile_type = int(profile_type)
        if(profile_type != VENDOR_NOT_APPROVED and profile_type != VENDOR_APPROVED and profile_type != BUYER):
            return Response({'error':'Falha na requisição'}, status=HTTP_400_BAD_REQUEST)

        if(photo_data):
            photo = cloudinary.uploader.upload(photo_data, transformation = [
                {'width': 1024, 'height': 1024, 'crop': 'fit'}, 
            ])
            photo_url = photo['url']

        else:
            photo_url = DEFAULT_PHOTO
        location = Location()
        location.save()
        profile = Profile(user=user, name=name, photo=photo_url, profile_type=profile_type, location=location)
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(data=serializer.data,status=HTTP_200_OK)


@api_view(["POST"])
def update_profile(request):
    #Requests
    jwt_token = request.data.get('token')
    name = request.data.get('name')
    photo_data = request.data.get('photo')
    profile_type = request.data.get('profile_type')

    try:
        user_json = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
        username = user_json['username']
        user = User.objects.get(username = username)
    except:
        return Response({'error':'Usuário não identificado'}, status=HTTP_403_FORBIDDEN)

    try:
        profile = Profile.objects.get(user=user)

    except Profile.DoesNotExist:
        return Response({'error':'Perfil não encontrado'}, status=HTTP_404_NOT_FOUND)

    if(name):
        profile.name=name
        profile.save()
    if(photo_data):
        photo = cloudinary.uploader.upload(photo_data, transformation = [
                {'width': 1024, 'height': 1024, 'crop': 'fit'}, 
            ])
        photo_url = photo['url']
        profile.photo=photo_url
        profile.save()

    if(profile_type):
        profile_type = int(profile_type)
        if(profile_type == VENDOR_NOT_APPROVED or profile_type == VENDOR_APPROVED or profile_type == BUYER):
            profile.profile_type = profile_type
            profile.save()

    serializer = ProfileSerializer(profile)
    return Response(data=serializer.data,status=HTTP_200_OK)

