from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category, Review, ProductImage
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from product.pagination import DefaultPagination
from api.permissions import IsAdminOrReadOnly, FullDJandoModelPermission
from product.permissions import IsReviewAuthorOrReadonly



class ProductViewSets(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    permission_classes = [IsAdminOrReadOnly]

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs['product_id'])

    def perform_create(self, serializer):
        serializer.save(product_id = self.kwargs['product_id'])

class CategoryViewSets(ModelViewSet):   
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count = Count('products')).all()
    serializer_class = CategorySerializer
    


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs['product_id'],
        }