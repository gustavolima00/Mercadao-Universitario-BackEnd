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