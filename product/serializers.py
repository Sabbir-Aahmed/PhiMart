from rest_framework import serializers
from decimal import Decimal
from product.models import Category, Product, Review
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'product_count'
        ]
    
    product_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='category-detail'
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'category', 'price_with_tax'
        ]

    def calculate_tax(self, product):
        from decimal import Decimal
        return round(product.price * Decimal(1.1), 2)
    
    def validate_price(self,price):
        if price < 0:
            raise serializers.ValidationError('Price could not be negative')
        return price
    
    # def object_validation(self,attrs):
    #     if attrs['password1'] != attrs['password2']:
    #         raise serializers.ValidationError("Password didn't pass")

class SimpleUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'full_name'
        ]

    def get_current_user_name(self,obj):
        return obj.get_full_name()
    
class ReviewSerializer(serializers.ModelSerializer):
    # user = SimpleUserSerializer()
    user = serializers.SerializerMethodField(method_name='get_user')

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'ratings', 'comment']
        read_only_fields = ['user', 'product']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)