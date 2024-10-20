from django.db import models
from subscriptions.models import Subscription
# Create your models here.

class User(models.Model):
    phone_number = models.CharField(max_length=20)  
    first_name = models.CharField(max_length=255)  
    last_name = models.CharField(max_length=255, null=True, blank=True) 
    city = models.CharField(max_length=255) 

    def __str__(self):
        return self.first_name

class Child(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=255)  
    last_name = models.CharField(max_length=255, null=True, blank=True)  
    birth_date = models.DateField()  
    gender = models.CharField(max_length=10) 

    def __str__(self):
        return self.first_name

class UserSubscription(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)  
    child = models.ForeignKey(Child, on_delete=models.CASCADE)  
    subscription_type = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    activation_date = models.DateTimeField()  
    expiration_date = models.DateTimeField()  
    total_days = models.PositiveIntegerField() 
    freeze_days = models.PositiveIntegerField() 
    remaining_freeze_days = models.PositiveIntegerField() 

    def __str__(self):
        return f"{self.child.first_name} | {self.subscription_type} | {self.parent.first_name}"


