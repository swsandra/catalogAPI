from rest_framework import routers

from .views import APIRootView

class CustomRouter(routers.DefaultRouter):
    """
    Extends the DefaultRouter, tu use custom API root view.
    """
    APIRootView = APIRootView