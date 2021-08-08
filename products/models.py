from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

class User(AbstractUser):
    """ User model. Extends from Django User model.
        This model requires user's email.
    """
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True
    )

class Brand(models.Model):
    """ Brand model
    
    Attributes:
    + name
    """
    name = models.CharField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name

    def get_info_str(self):
        """ Returns brand information as a string """
        return f"Brand information:\n\tname: {self.name}\n"
    
    def changed(self, old_self):
        """ Compares self to old instance, field by field, to determine if
            self has changed.
            
            Returns bool indicating if self has changed."""
        return self.name != old_self.name
    
    def get_updated_info_str(self, old_self):
        """ Returns updated information as a string """
        info_str = ""
        if self.name != old_self.name:
            info_str += f"\n\tname: {old_self.name} -> {self.name}"
        return info_str

class Product(models.Model):
    """ Product model

    Attributes:
    + sku
    + name
    + price
    + brand
    + visits
    """
    sku = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="SKU"
    )
    name = models.CharField(
        max_length=255
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))])
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products"
    )
    visits = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def update_visits(self):
        """ Updates visits count """
        self.visits += 1
        self.save()

    def get_info_str(self):
        """ Returns product information as a string """
        return "Product information:\n" + \
                f"\tSKU: {self.sku}\n" + \
                f"\tname: {self.name}\n" + \
                f"\tprice: {self.price}\n" + \
                f"\tbrand: {self.brand}\n"
    
    def changed(self, old_self):
        """ Compares self to old instance, field by field, to determine if
            self has changed.
            
            Returns bool indicating if self has changed."""
        return self.sku != old_self.sku or self.name != old_self.name \
            or self.price != old_self.price or self.brand != old_self.brand

    def get_updated_info_str(self, old_self):
        """ Returns updated information as a string """
        info_str = ""
        if self.sku != old_self.sku:
            info_str += f"\n\tSKU: {old_self.sku} -> {self.sku}"
        if self.name != old_self.name:
            info_str += f"\n\tname: {old_self.name} -> {self.name}"
        if self.price != old_self.price:
            info_str += f"\n\tprice: {old_self.price} -> {self.price}"
        if self.brand != old_self.brand:
            info_str += f"\n\tbrand: {old_self.brand} -> {self.brand}"
        return info_str
