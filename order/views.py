from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from order.models import Cart,CartItem,Order,OrderItem
from order.serializers import CartSerializer,CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer,EmptySerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        if created:
            serializer.instance = cart
        else:
            raise ValidationError("You already have a cart.")
        
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)

    @swagger_auto_schema(
        operation_summary='Create a new cart',
        operation_description="Create a new cart for the authenticated user. A user can only have one active cart.",
        request_body=CartSerializer,
        responses={201: CartSerializer, 400: 'Cart already exists'}
    )
    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()

        if existing_cart:
            serializer = self.get_serializer(existing_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return super().create(request,*args,**kwargs)


    swagger_auto_schema(
        operation_summary="Retrieve user's cart",
        operation_description="Retrieve the authenticated user's cart."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
      
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        return {'cart_id': self.kwargs.get('cart_pk')}
  

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs.get('cart_pk'))


    @swagger_auto_schema(
        operation_summary="Add product to cart",
        operation_description="Add a product to the cart.",
        request_body=AddCartItemSerializer,
        responses={201: CartItemSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update cart item quantity",
        operation_description="Update the quantity of an item in the cart.",
        request_body=UpdateCartItemSerializer,
        responses={200: CartItemSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
class OrderViewSet(ModelViewSet):
    http_method_names = ['get','delete','patch', 'post', 'head', 'options']
    
    @swagger_auto_schema(
        operation_summary="Cancel order",
        operation_description="Cancel the specified order.",
        request_body=EmptySerializer,
        responses={200: openapi.Response('Order canceled')}
    )

    @action(detail=True, methods=['post'])
    def cancel(self,request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user = request.user)
        return Response({'status': 'Order Canceled'})

    @swagger_auto_schema(
        operation_summary="Update order status",
        operation_description="Update the status of an order (Admin only).",
        request_body=UpdateOrderSerializer,
        responses={200: openapi.Response('Order status updated')}
    )

    @action(detail=True, methods=['patch'])
    def update_status(self,request,pk=None):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order, data=request.data, partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Order status updated to {request.data['status']}"})

    
    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'update_status':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)

    