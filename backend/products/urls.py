from django.urls import include, path
from . import views

urlpatterns = [
    path('create_product/', views.create_product),
]