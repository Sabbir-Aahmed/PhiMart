from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer
from django.db.models import Count



@api_view(['GET', 'POST'])
def view_product(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many = True, context={'request': request})
        return Response(serializer.data)
    if request.method=='POST':
        serializer = ProductSerializer(data=request.data, context={'request': request}) #deserializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def view_specefic_products(request,id):
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    if request.method == 'PUT':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        product = get_object_or_404(Product, pk=id)
        copy_of_product = product
        serializer = ProductSerializer(copy_of_product, context = {'request': request})
        product.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def view_categories(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(product_count = Count('products')).all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = CategorySerializer(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
        

@api_view(['GET', 'PUT', 'DELETE'])
def view_specefic_category(request, pk):
    if request.method == 'GET':
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    if request.method == 'PUT':
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    if request.method == 'DELETE':
        category = get_object_or_404(Category, pk=pk)
        copy_of_category = category
        serializer = CategorySerializer(copy_of_category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)