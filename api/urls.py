from django.urls import path,include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSets, CategoryViewSets

router = DefaultRouter()
router.register('products', ProductViewSets)
router.register('categories', CategoryViewSets, basename='category')

urlpatterns = router.urls