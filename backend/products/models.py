from django.db import models

class Product(models.Model):
    created = models.DateTimeField(auto_now_add= True)
    vendor_id = models.IntegerField()
    name = models.TextField()
    price = models.FloatField()
    photo = models.TextField()
