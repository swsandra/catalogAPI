from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import serializers

from .models import Brand, Product, User

class UserSerializer(serializers.ModelSerializer):
    """ User serializer """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email' )
        read_only_fields = ('id', )

class UserRegistrationSerializer(UserSerializer):
    """ User registration serializer """
    password = serializers.CharField(style={'input_type': 'password'},
                                     allow_blank=False, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'},
                                             allow_blank=False, write_only=True)

    class Meta(UserSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'password', 'confirm_password')
        read_only_fields = ('id', )
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        """ Validates password """
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(list(exc))
        return value

    def is_valid(self, raise_exception=False):
        """ Validates password and password confirmation are received """
        if not self.initial_data.get('password') or not self.initial_data.get('confirm_password'):
            _err = {}
            if not self.initial_data.get('password'):
                _err['password'] = ['This field is required.']
            if not self.initial_data.get('confirm_password'):
                _err['confirm_password'] = ['Please confirm your password.']
            raise serializers.ValidationError(_err)

        if self.initial_data.get('password') != self.initial_data.get('confirm_password'):
            _err = {'error': 'Passwords do not match.'}
            raise serializers.ValidationError(_err)

        return super(UserRegistrationSerializer, self).is_valid(raise_exception)

    def create(self, validated_data):
        """ User creation """
        serializers.raise_errors_on_nested_writes('create', self, validated_data)

        instance = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Full name
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        instance.save()

        return instance

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