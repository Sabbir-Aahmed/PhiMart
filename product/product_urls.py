from django.urls import path, include
from product import views

urlpatterns = [
    path('', views.ViewProducts.as_view(), name = 'product-list'),
    path('<int:id>/', views.ViewSpeceficProduct.as_view(), name='products-list'),
     
]