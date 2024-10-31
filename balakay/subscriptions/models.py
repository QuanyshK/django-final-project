from django.db import models

class AgeGroup(models.Model):
    age_range = models.CharField(max_length=20)  # e.g., "0-4", "4-7", "7-16"
    description = models.CharField(max_length=255, blank=True, null=True)  # optional description for the age group

    def __str__(self):
        return self.age_range

class Subscription(models.Model):
    active = models.BooleanField(default=True) 
    name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    duration_text = models.CharField(max_length=255) 
    age_group = models.ForeignKey(AgeGroup, on_delete=models.SET_NULL, null=True, related_name="subscriptions")  
    total_days = models.PositiveIntegerField()  
    freeze_days = models.PositiveIntegerField()  
    daily_visits = models.PositiveIntegerField()  
    monthly_visits = models.PositiveIntegerField()  
    premium_monthly_visits = models.PositiveIntegerField()  

    def __str__(self):
        return self.name
