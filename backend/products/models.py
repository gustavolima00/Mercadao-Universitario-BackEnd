from django.db import models
from profiles.models import Profile

class Product(models.Model):
    created = models.DateTimeField(auto_now_add= True)
    vendor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.TextField()
    price = models.FloatField()
    photo = models.TextField()
