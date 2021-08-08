from rest_framework import routers

from .views import APIRootView

class CustomRouter(routers.DefaultRouter):
    """
    Extends the DefaultRouter, to use custom API root view.
    """
    APIRootView = APIRootView