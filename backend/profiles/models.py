from django.db import models
from django.contrib.auth.models import User

VENDOR_NOT_APPROVED = 2
VENDOR_APPROVED = 3
BUYER = 1

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=30, blank=True)
    photo = models.TextField(blank=True)
    profile_type = models.IntegerField( default=BUYER )
