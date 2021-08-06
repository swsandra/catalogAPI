from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Brand, Product

from .serializers import BrandSerializer, ProductSerializer, ProductSerializerForAnon

class BrandViewSet(viewsets.ModelViewSet):
    """
    create:
        
    retrieve:
        
    update:
        
    delete:
        
    """
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated, )

class ProductViewSet(viewsets.ModelViewSet):
    """
    create:
        
    retrieve:
        
    update:
        
    delete:
        
    """
    queryset = Product.objects.all().order_by("name")
    # serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        """  """
        if self.action in ['list', 'retrieve']: # Anyone can retrieve products
            self.permission_classes = (AllowAny, )
        return super(ProductViewSet, self).get_permissions()

    def get_serializer_class(self):
        """  """
        if self.request.user.is_anonymous:
            return ProductSerializerForAnon
        return ProductSerializer