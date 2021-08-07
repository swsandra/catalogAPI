from django.urls import path

from rest_framework import routers

from .views import BrandViewSet, ProductViewSet, UserViewSet, ChangePasswordView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('api/users/change-password',
        ChangePasswordView.as_view(), name='change_password'),
]
