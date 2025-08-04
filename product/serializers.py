from rest_framework import serializers
from decimal import Decimal
from product.models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'product_count'
        ]
    
    product_count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='view_specefic_category'
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'category', 'price_with_tax'
        ]

    def calculate_tax(self, product):
        from decimal import Decimal
        return round(product.price * Decimal(1.1), 2)
