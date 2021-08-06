from django.shortcuts import render
from django.db import transaction

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Brand, Product, User

from .serializers import (BrandSerializer, ProductSerializer, ProductSerializerForAnon, 
    UserSerializer)

class UserViewSet(viewsets.ModelViewSet):
    """ Viewset for brands """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

class BrandViewSet(viewsets.ModelViewSet):
    """ Viewset for brands """
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated, )

class ProductViewSet(viewsets.ModelViewSet):
    """ Viewset for products """
    queryset = Product.objects.all().order_by("name")
    # serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        """ Get permissions for views.
            Any user can list or retrieve products, admins can perform the rest of
            the actions too. """
        if self.action in ['list', 'retrieve']: # Anyone can retrieve products
            self.permission_classes = (AllowAny, )
        return super(ProductViewSet, self).get_permissions()

    def get_serializer_class(self):
        """ Get serializer by user.
            Anonymous users cannot see database ID nor product visits. """
        if self.request.user.is_anonymous:
            return ProductSerializerForAnon
        return ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        """ Retrieving a product.
            When an anonymous user retrieves a product, increase visits. """
        instance = self.get_object()
        if self.request.user.is_anonymous:
            with transaction.atomic(): # To prevent DB inconsistencies
                instance.update_visits()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
