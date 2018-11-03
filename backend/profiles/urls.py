from django.urls import include, path
from . import views

urlpatterns = [
    path('create_profile/', views.create_profile),
    path('update_profile/', views.update_profile),
]