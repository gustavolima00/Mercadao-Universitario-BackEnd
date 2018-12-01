from django.db import models

#Order status
# open close

class Order(models.Model):
    created = models.DateTimeField(auto_now_add= True)
    vendor_id = models.IntegerField()
    buyer_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    status = models.TextField()
# Create your models here.
