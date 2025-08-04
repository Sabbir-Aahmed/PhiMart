from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer

@api_view()
def view_product(request):
    products = Product.objects.select_related('category').all()
    serializer = ProductSerializer(products, many = True, context={'request': request})
    return Response(serializer.data)

@api_view()
def view_specefic_products(request,id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
    

@api_view()
def view_categories(request):
    return Response({"response" : "categories"})

@api_view()
def view_specefic_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)