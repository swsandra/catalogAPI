from django.contrib import admin
from .models import Brand, Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """ Admin for brands """
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin for products """
    list_display = ('id', 'sku', 'name', 'price', 'brand', 'visits')