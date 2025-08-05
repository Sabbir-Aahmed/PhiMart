from django.urls import path, include
from product import views

urlpatterns = [
    path('', views.ViewCategories.as_view(), name='category-list'),
    path('<int:pk>/', views.ViewSpeceficCategory.as_view(), name= 'view_specefic_category')
     
]