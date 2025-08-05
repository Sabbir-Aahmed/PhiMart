from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category, Review
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.viewsets import ModelViewSet


class ProductViewSets(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category_id','price']
    filterset_class = ProductFilter

    # def get_queryset(self):
    #     queryset = Product.objects.select_related('category').all()
    #     category_id = self.request.query_params.get('category_id')

    #     if category_id is not None:
    #         queryset = Product.objects.filter(category_id=category_id)

    #     return queryset
    
    def delete(self,request,*args, **kwargs):
        product = self.get_object()
        if product.stock > 10:
            return Response({"message": "Product with stock more than 10 could not be deleted"})
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)



class CategoryViewSets(ModelViewSet):
    queryset = Category.objects.annotate(product_count = Count('products')).all()
    serializer_class = CategorySerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}