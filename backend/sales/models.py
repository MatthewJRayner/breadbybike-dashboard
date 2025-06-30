from django.db import models

# Create your models here.
class OrderLine(models.Model):
    """
    Represents a single order line for each order grabbed from Square.
    This model is used to store detailed information about each order,
    including the name, date, time, location, quantity, and financial details.
    """
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
            models.Index(fields=['location']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"Order {self.name} x{self.quantity} at {self.time} {self.date} ({self.location})"
    
class OrderStats(models.Model):
    """
    Stores all statistics that will be used on the frontend.
    This model is designed to be updated periodically with precomputed stats
    to reduce load on the database and speed up frontend rendering.
    The stats are stored in JSON format to allow for flexible and dynamic data structures.
    The 'location' field uniquely identifies the data block, e.g.:
        - both_home_stats
        - bakery_home_stats
        - cafe_home_stats
        etc.
    """
    location = models.CharField(max_length=100, unique=True)
    stats_json = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [models.Index(fields=['location'])]
    
    def __str__(self):
        return f"Stats for {self.location} - Last updated at {self.updated_at}"