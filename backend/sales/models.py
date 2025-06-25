from django.db import models

# Create your models here.
class OrderLine(models.Model):
    name = models.CharField(max_length=255, default='Custom')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    total_sale = models.DecimalField(max_digits=10, decimal_places=2)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        indexes = [
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"Order {self.name} x{self.quantity} at {self.time} {self.date} ({self.location})"