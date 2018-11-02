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

# Create your tests here.
