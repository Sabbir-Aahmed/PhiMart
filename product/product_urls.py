from django.urls import path, include
from product import views

urlpatterns = [
    path('', views.view_product, name = 'product-list'),
    path('<int:id>/', views.view_specefic_products, name='products-list'),
     
]