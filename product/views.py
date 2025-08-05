from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('category').all()
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    # def delete(self,request,id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.stock > 10:
    #         return Response({"message": "Product with stock more than 10 could not be deleted"})
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class ViewSpeceficProduct(APIView):
    def get(self,request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def put(self,request,id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,id):
        product = get_object_or_404(Product, pk=id)
        copy_of_product = product
        serializer = ProductSerializer(copy_of_product, context = {'request': request})
        product.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    

class CategoryList(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count = Count('products')).all()
    serializer_class = CategorySerializer

class ViewSpeceficCategory(APIView):
    def get(self,request,pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self,request,pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self,request,pk):
        category = get_object_or_404(Category, pk=pk)
        copy_of_category = category
        serializer = CategorySerializer(copy_of_category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)