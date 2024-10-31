from django.db import models
from subscriptions.models import Subscription
from django.contrib.auth.models import  User
from django.utils import timezone
from datetime import timedelta

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)  
    city = models.CharField(max_length=255) 
    def __str__(self):
        return self.first_name

class Child(models.Model):
    parent = models.ForeignKey(Client, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=255)  
    last_name = models.CharField(max_length=255, null=True, blank=True)  
    birth_date = models.DateField()  
    gender = models.CharField(max_length=10) 

    def __str__(self):
        return self.first_name


class UserSubscription(models.Model):
    parent = models.ForeignKey(Client, on_delete=models.CASCADE)  
    child = models.ForeignKey(Child, on_delete=models.CASCADE)  
    subscription_type = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    activation_date = models.DateTimeField()  
    expiration_date = models.DateTimeField()  
    total_days = models.PositiveIntegerField() 
    freeze_days = models.PositiveIntegerField() 
    daily_visits_limit = models.PositiveIntegerField()
    total_visits = models.PositiveIntegerField()
    used_visits = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.child.first_name} | {self.subscription_type} | {self.parent.first_name}"

    def update_remaining_days_and_visits(self):
        today = timezone.now()
    
        if self.is_active and today >= self.activation_date:
            days_passed = (today - self.activation_date).days
        
        if days_passed > 0:  
            self.total_days = max(0, self.total_days - days_passed)
            self.remaining_freeze_days = max(0, self.remaining_freeze_days - days_passed)

            if self.total_days <= 0:
                self.is_active = False
                self.expiration_date = today
                self.total_days = 0
            else:
                self.expiration_date = self.activation_date + timedelta(days=self.total_days)
        
        self.save()


