from django.urls import path, include
from product import views

urlpatterns = [
    path('', views.view_categories, name='category-list'),
     
]