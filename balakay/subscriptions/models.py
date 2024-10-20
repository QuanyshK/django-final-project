from django.db import models

# Create your models here.

class Subscription(models.Model):
    active = models.BooleanField(default=True) 
    name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    duration_text = models.CharField(max_length=255) 
    age_group = models.CharField(max_length=50)  
    total_days = models.PositiveIntegerField()  
    freeze_days = models.PositiveIntegerField()  
    daily_visits = models.PositiveIntegerField()  
    monthly_visits = models.PositiveIntegerField()  
    premium_monthly_visits = models.PositiveIntegerField()  

    def __str__(self):
        return self.name