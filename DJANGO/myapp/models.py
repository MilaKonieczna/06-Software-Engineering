from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def positive(value):
    if value <= 0:
        raise ValidationError('Value must be positive')


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        validators=[positive]
    )
    available = models.BooleanField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed')
    ]

    status = models.CharField(choices=STATUS_CHOICES, max_length=11, default='New')

    def __str__(self):
        return f"Order {self.id} - {self.customer.name}"

    def total_price(self):
        return sum(p.price for p in self.products.all())

    def fulfilled(self):
        return all(p.available for p in self.products.all())
