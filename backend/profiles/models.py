from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=30, blank=True)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        self.save()
        
# Create your models here.
