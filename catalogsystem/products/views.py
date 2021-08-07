from django.db import transaction

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Brand, Product, User
from .utils import send_email_notification

from .serializers import (BrandSerializer, ProductSerializer, ProductSerializerForAnon, 
    UserSerializer, UserRegistrationSerializer, ChangePasswordSerializer)

class UserViewSet(viewsets.ModelViewSet):
    """ Viewset for users """
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        """ Get User serializer by action. """
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer

class ChangePasswordView(generics.UpdateAPIView):
    """ Updates user's password """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, )

    def get_object(self, queryset=None):
        """ Gets current user """
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        """ Updates password """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.validated_data.get("old_password")):
                _err = {"old_password": ["Wrong password."]}
                return Response(_err, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes user's password
            self.object.set_password(serializer.validated_data.get("password"))
            self.object.save()
            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseViewSet(viewsets.ModelViewSet):
    """ Base viewset for brands and products. To allow notifications on updates/deletions """

    def update(self, request, *args, **kwargs):
        """ Updates instance and sends email to notify other users """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_instance = self.get_object() # To notify changes
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # Send email notification
        send_email_notification(self.request.user, old_instance, instance)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """ Deletes instance and sends email to notify other users """
        instance = self.get_object()
        self.perform_destroy(instance)
        # Send email notification
        send_email_notification(self.request.user, instance, None, False)
        return Response(status=status.HTTP_204_NO_CONTENT)

class BrandViewSet(BaseViewSet):
    """ Viewset for brands """
    queryset = Brand.objects.all().order_by("name")
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated, )

class ProductViewSet(BaseViewSet):
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
