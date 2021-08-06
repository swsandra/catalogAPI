from django.urls import path

from rest_framework import routers

from .views import BrandViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')
