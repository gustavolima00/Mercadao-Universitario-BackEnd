from django.urls import include, path

urlpatterns = [
    path('rest-auth/', include('backend.auth_urls')),
    path('profiles/', include('profiles.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
]
