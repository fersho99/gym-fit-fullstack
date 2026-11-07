from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]
from .views import precio_final

urlpatterns += [
    path('products/<int:pk>/precio-final/', precio_final, name='product-precio-final'),
]
