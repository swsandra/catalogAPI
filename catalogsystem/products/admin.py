from django.contrib import admin
from .models import Brand, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """ Brands admin """
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Products admin """
    list_display = ('id', 'sku', 'name', 'price', 'brand', 'visits')