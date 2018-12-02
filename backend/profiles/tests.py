from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Profile
from django.contrib.auth.models import User
from .serializers import ProfileSerializer

class CheckProfileViewTest(APITestCase):
    def test_create_profile(self):
        user_request = {
            'password1':'abc123abc123', 
            'password2':'abc123abc123', 
            'email': 'test_create_profile@teste.com',
            'username': 'test_create_profile'
        }
        register_response = self.client.post('/rest-auth/registration/', user_request)
        token=register_response.json()['token']
        
        #Invalid Token request
        request_1 = {'jwt_token': 'invalid_token'}
        response_1 = self.client.post('/profiles/create_profile/', request_1)
        self.assertEqual(response_1.status_code, 403)
        self.assertEqual(response_1.json(), {'error':'Usuário não identificado'})

        # No name in request
        request_2 = {'jwt_token': token}
        response_2 = self.client.post('/profiles/create_profile/', request_2)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_2.json(), {'error':'Falha na requisição'})

        #If is ok 
        request_3 = {'jwt_token': token, 'name':'sample_name'}
        response_3 = self.client.post('/profiles/create_profile/', request_3)
        user = User.objects.get(username = 'test_create_profile')
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        self.assertEqual(response_3.status_code, 200)
        self.assertEqual(response_3.json(), serializer.data)

    def test_update_profile(self):
        user_request = {
            'password1':'abc123abc123', 
            'password2':'abc123abc123', 
            'email': 'test_update_profile@teste.com',
            'username': 'test_update_profile'
        }
        register_response = self.client.post('/rest-auth/registration/', user_request)
        token=register_response.json()['token']
        #Profile does not exist
        request_1 = {'jwt_token': token, 'name': 'new_name'}
        response_1 = self.client.post('/profiles/update_profile/', request_1)
        self.assertEqual(response_1.status_code, 404)
        self.assertEqual(response_1.json(), {'error':'Perfil não encontrado'})
        
        #Creation of profile
        profile_request = {'jwt_token':token,'name': 'test_update_profile'}
        profile_response = self.client.post('/profiles/create_profile/', profile_request)
        
        #Invalid Token request
        request_2 = {'jwt_token': 'invalid_token'}
        response_2 = self.client.post('/profiles/update_profile/', request_2)
        self.assertEqual(response_2.status_code, 403)
        self.assertEqual(response_2.json(), {'error':'Usuário não identificado'})

        #If it is ok 
        request_3 = {'jwt_token': token, 'name': 'new_name'}
        response_3 = self.client.post('/profiles/update_profile/', request_3)
        self.assertEqual(response_3.status_code, 200)
        user = User.objects.get(username = 'test_update_profile')
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        self.assertEqual(response_3.json(), serializer.data)