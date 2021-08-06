from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Brand, Product

class UserSerializer(serializers.ModelSerializer):
    """ User serializer """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email' )
        read_only_fields = ('id', )

class BrandSerializer(serializers.ModelSerializer):
    """ Brand serializer """
    class Meta:
        model = Brand
        fields = ('id', 'name')
        read_only_fields = ('id', )

class ProductSerializer(serializers.ModelSerializer):
    """ Product serializer """
    class Meta:
        model = Product
        fields = ('id', 'sku', 'name', 'price', 'brand', 'visits')
        read_only_fields = ('id', 'visits') # Admins can't change visits

class ProductSerializerForAnon(serializers.ModelSerializer):
    """ Product serializer for anonymous users """
    class Meta:
        model = Product
        fields = ('sku', 'name', 'price', 'brand')
        read_only_fields = fields