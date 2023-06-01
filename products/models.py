from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class Review(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    grade = models.DecimalField(max_digits=1, decimal_places=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.title
