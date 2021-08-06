from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

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
