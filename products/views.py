from collections import OrderedDict

from django.db import transaction
from django.urls import NoReverseMatch

from rest_framework import viewsets, status, routers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Brand, Product, User
from .utils import send_email_notification

from .serializers import (BrandSerializer, ProductSerializer, ProductSerializerForAnon, 
    UserSerializer, UserRegistrationSerializer, ChangePasswordSerializer, ProductListSerializer)

class APIRootView(routers.APIRootView):
    """
    Api Root View.
    """
    permission_classes = (AllowAny, )

    def get(self, request, *args, **kwargs):
        """ Implements base routers.APIRootView.get(), adding pop of users and brands endpoints """
        # Return a plain {"name": "hyperlink"} response.
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format')
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue
        if self.request.user.is_anonymous:
            ret.pop("users")
            ret.pop("brands")
        return Response(ret)

class UserViewSet(viewsets.ModelViewSet):
    """ Viewset for users """
    queryset = User.objects.all()
    # serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        """ Get User serializer by action. """
        if self.action == 'create':
            return UserRegistrationSerializer
        if self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """ Updates user's password """
        serializer = self.get_serializer(data=request.data)
        user = self.request.user

        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.validated_data.get("old_password")):
                _err = {"old_password": ["Wrong password."]}
                return Response(_err, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes user's password
            user.set_password(serializer.validated_data.get("password"))
            user.save()
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
    queryset = Brand.objects.all().order_by("id")
    serializer_class = BrandSerializer
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """ Gets all brand products """
        brand = self.get_object()
        serializer = ProductSerializer(brand.products.all(), many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductViewSet(BaseViewSet):
    """ Viewset for products """
    queryset = Product.objects.all().order_by("id")
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
        if self.action in ['list', 'retrieve']:
            return ProductListSerializer
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
