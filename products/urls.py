from django.urls import path

# from rest_framework import routers
from .routers import CustomRouter
from .views import BrandViewSet, ProductViewSet, UserViewSet

# router = routers.DefaultRouter()
router = CustomRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [

]
