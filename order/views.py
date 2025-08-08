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
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
      
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
  

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id = self.kwargs['cart_pk'])


class OrderViewSet(ModelViewSet):
    http_method_names = ['get','delete','patch', 'post', 'head', 'options']
    
    @action(detail=True, methods=['post'], permission_classes = [IsAuthenticated])
    def cancel(self,request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user = request.user)
        return Response({'status': 'Order Canceled'})

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'user': self.request.user}
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
