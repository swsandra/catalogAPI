from django.urls import path

from rest_framework import routers

from .views import BrandViewSet, ProductViewSet, UserViewSet, ChangePasswordView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'products', ProductViewSet, basename='product')

router.get_api_root_view().cls.__doc__ = \
    ("Api Root View.\n\nusers: Endpoint for users.\nbrands: Endpoint for brands.\nproducts: Endpoint for products.")

urlpatterns = [
    path('api/users/change-password',
        ChangePasswordView.as_view(), name='change_password'),
]
