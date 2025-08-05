from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count
from rest_framework.views import APIView



class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many = True, context={'request': request})
        return Response(serializer.data)

    def post(self,request):
        serializer = ProductSerializer(data=request.data, context={'request': request}) #deserializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

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
    


class ViewCategories(APIView):
    def get(self,request):
        categories = Category.objects.annotate(product_count = Count('products')).all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = CategorySerializer(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    

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