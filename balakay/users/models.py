from django.db import models
from subscriptions.models import Subscription
from django.contrib.auth.models import  User
from django.utils import timezone
from datetime import timedelta

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)  

    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20,  
 unique=True)  
    city = models.CharField(max_length=255) 

    def __str__(self):
        return self.first_name

class Child(models.Model):
    parent = models.ForeignKey(Client, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=255)  
    last_name = models.CharField(max_length=255,  
 null=True, blank=True)  
    birth_date = models.DateField()  
  
    gender = models.CharField(max_length=10) 

    def __str__(self):
        return self.first_name

class UserSubscription(models.Model):
    parent = models.ForeignKey(Client, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    subscription_type = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    activation_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(null=True, blank=True)
    total_days = models.PositiveIntegerField()
    freeze_days = models.PositiveIntegerField(default=40)
    daily_visits_limit = models.PositiveIntegerField(default=2)
    total_visits = models.PositiveIntegerField(default=30)
    used_visits = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(used_visits__lte=models.F('total_visits')),
                name='used_visits_lte_total_visits'
            ),
        ]

    def __str__(self):
        return f"{self.child.first_name} | {self.subscription_type} | {self.parent.first_name}"

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            self.expiration_date = self.activation_date + timedelta(days=self.total_days)
        self.update_remaining_days_and_visits()
        super().save(*args, **kwargs)

    def update_remaining_days_and_visits(self):
        today = timezone.now()
        if self.is_active and today >= self.activation_date:
            days_passed = (today - self.activation_date).days
            self.total_days = max(0, self.total_days - days_passed)
            if self.total_days <= 0:
                self.is_active = False
                self.expiration_date = today  # Set expiration_date to today when subscription becomes inactive
            else:
                self.expiration_date = self.activation_date + timedelta(days=self.total_days)
        # Ensure used_visits never exceeds total_visits
        self.used_visits = min(self.total_visits, self.used_visits) 

    def record_visit(self):
        if self.is_active and self.total_visits > 0:
            self.used_visits += 1
            self.total_visits -= 1
            self.save()
