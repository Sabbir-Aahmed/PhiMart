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
from drf_yasg.utils import swagger_auto_schema


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

    @swagger_auto_schema(
        operation_summary='Retrive a list of products'
    )

    def list(self, request, *args, **kwargs):
        """Retrive all the products"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a product by admin',
        operation_description="This allow an admin to create a product",
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)
    
class ProductImageViewSet(ModelViewSet):
    """
    Handles image uploads and retrieval for a specific product.
    """
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs.get('product_id'))

    def perform_create(self, serializer):
        serializer.save(product_id = self.kwargs.get('product_id'))

    @swagger_auto_schema(
        operation_summary="List product images",
        operation_description="Retrieve all images for a specific product ID.",
        responses={200: ProductImageSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Upload a new product image",
        operation_description="Upload an image for a specific product by providing the image file.",
        request_body=ProductImageSerializer,
        responses={201: ProductImageSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class CategoryViewSets(ModelViewSet):
    """
    Manage product categories.
    """   
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(product_count = Count('products')).all()
    serializer_class = CategorySerializer
    

    @swagger_auto_schema(
        operation_summary="List categories",
        operation_description="Retrieve a list of all categories with the number of products in each.",
        responses={200: CategorySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a category",
        request_body=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    """
    Manage reviews for a specific product.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_id'))

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs.get('product_id'),
        }
    
    @swagger_auto_schema(
        operation_summary="List product reviews",
        operation_description="Retrieve all reviews for a specific product ID.",
        responses={200: ReviewSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add a review",
        operation_description="Add a review for a specific product. The logged-in user will be automatically assigned.",
        request_body=ReviewSerializer,
        responses={201: ReviewSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)