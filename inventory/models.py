from django.db import models

class UniformItem(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name