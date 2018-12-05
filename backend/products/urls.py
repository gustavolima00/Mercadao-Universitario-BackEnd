from django.urls import include, path
from . import views

urlpatterns = [
    path('create_product/', views.create_product),
    path('delete_product/', views.delete_product),
    path('edit_product/', views.edit_product),
    path('get_product/', views.get_product),
    path('all_products/', views.all_products),
    path('user_products/', views.user_products),
    path('nearby_products/', views.nearby_products),
    path('search_products/', views.search_products),
]