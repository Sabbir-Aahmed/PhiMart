from django.urls import path, include
from product import views

urlpatterns = [
    path('<int:id>', views.view_specefic_products, name='products-list'),
     
]