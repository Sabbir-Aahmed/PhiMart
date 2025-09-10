from django.urls import path,include
from product.views import ProductViewSets, CategoryViewSets, ReviewViewSet, ProductImageViewSet
from rest_framework_nested import routers
from order.views import CartViewSet, CartItemViewSet, OrderViewSet, initiate_payment, payment_success, payment_cancel,payment_fail, HasOrderedProduct

router = routers.DefaultRouter()
router.register('products', ProductViewSets , basename='products')
router.register('categories', CategoryViewSets, basename='category')
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewSet, basename='orders')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewSet, basename='product-image')

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup = 'cart')
cart_router.register('items', CartItemViewSet, basename = 'cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate/',initiate_payment, name="initiate_payment" ),
    path('payment/success/',payment_success, name="payment_success" ),
    path('payment/fail/',payment_fail, name="payment_fail" ),
    path('payment/cancel/',payment_cancel, name="payment_cancel" ),
    path('orders/has_ordered/<int:product_id>/',HasOrderedProduct.as_view() ),
]