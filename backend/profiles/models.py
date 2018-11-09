from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=30, blank=True)
    photo = models.TextField(blank=True)
    seller = models.BooleanField(default=False)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.save()

    def get_photo(self):
        return self.photo
    
    def set_photo(self, photo):
        self.photo = photo
        self.save()

    def get_user(self):
        return self.user
    
    def set_seller(self):
        self.seller = True
        self.save()

    def set_buyer(self):
        self.seller = False  
        self.save()

    def is_seller(self):
        return self.seller

# Create your models here.
