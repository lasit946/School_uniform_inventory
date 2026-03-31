from django.db import models
from django.contrib.auth.models import User

class UniformItem(models.Model):
    SIZE_CHOICES = [
        ('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'),
        ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', '2XL'), ('XXXL', '3XL'), ('N/A', 'N/A'),
    ]
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.size})"

class Sale(models.Model):
    item = models.ForeignKey(UniformItem, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField(default=1) # Tracks the "10 units"
    sale_date = models.DateTimeField(auto_now_add=True)
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)