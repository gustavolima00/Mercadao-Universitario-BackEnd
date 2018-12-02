from django.urls import include, path
from . import views

urlpatterns = [
    path('create_order/', views.create_order),
    path('vendor_orders/', views.vendor_orders),
    path('buyer_orders/', views.buyer_orders),
    path('set_order_status/', views.set_order_status),
    
]