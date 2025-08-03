from django.shortcuts import get_list_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product,Category
from rest_framework import status

@api_view()
def view_specefic_products(request,id):
    product = get_list_or_404(Product, pk=id)
    product_dic = {'Id': product.pk, 'Name': product.name, 'Price': product.price }
    return Response(product_dic)
    

@api_view()
def view_categories(request):
    return Response({"response" : "categories"})