from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Profile
from django.contrib.auth.models import User

class CheckProfileModelTest(APITestCase):
    def test_get_name(self):
        #Registro do usuário
        user = User.objects.create_user('test_get_name', 'test_get_name@teste.com', 'testpassword')

        #Criação do profile
        profile = Profile(user=user, name='test_get_name')
        profile_name = profile.get_name()

        self.assertEqual(profile_name, 'test_get_name')

    def test_set_name(self):
        #Registro do usuário
        user = User.objects.create_user('test_set_name', 'test_set_name@teste.com', 'testpassword')

        #Criação do profile
        profile = Profile(user=user, name='test_set_name')
        profile.set_name('new_name')
        profile_name = profile.get_name()

        self.assertEqual(profile_name, 'new_name')
    
    def test_get_photo(self):
        #Registro do usuário
        user = User.objects.create_user('test_get_photo', 'test_get_photo@teste.com', 'testpassword')

        #Criação do profile
        profile = Profile(user=user, photo='photo_url')
        profile_photo = profile.get_photo()

        self.assertEqual(profile_photo, 'photo_url')


    def test_set_photo(self):
        #Registro do usuário
        user = User.objects.create_user('test_set_photo', 'test_set_photo@teste.com', 'testpassword')

        #Criação do profile
        profile = Profile(user=user, photo='photo_url')
        profile.set_photo('new_photo_url')
        profile_photo = profile.get_photo()

        self.assertEqual(profile_photo, 'new_photo_url')

    def test_get_user(self):
        #Registro do usuário
        user = User.objects.create_user('test_get_user', 'test_get_user@teste.com', 'testpassword')

        #Criação do profile
        profile = Profile(user=user)
        profile_user = profile.get_user()

        self.assertEqual(profile_user, user)

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

        # No photo or user request
        request_2 = {'jwt_token': token}
        request_3 = {'jwt_token': token, 'name':'sample_name'}
        response_2 = self.client.post('/profiles/create_profile/', request_2)
        response_3 = self.client.post('/profiles/create_profile/', request_3)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(response_2.json(), {'error':'Falha na requisição'})
        self.assertEqual(response_3.json(), {'error':'Falha na requisição'})