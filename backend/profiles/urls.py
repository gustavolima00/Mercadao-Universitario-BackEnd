from django.urls import include, path
from . import views

urlpatterns = [
    path('create_profile/', views.create_profile),
]