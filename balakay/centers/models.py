from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)  #
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name
    
class Center(models.Model):
    manager_name = models.CharField(max_length=255)  
    manager_phone = models.CharField(max_length=20)  
    name = models.CharField(max_length=255)  
    logo = models.ImageField(upload_to='storage/')  
    subtitle = models.CharField(max_length=255, null=True, blank=True) 
    description = models.TextField()  
    city = models.CharField(max_length=255)  
    address = models.CharField(max_length=255) 

    def __str__(self):
        return self.name

class Section(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE) 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='sections')
    name = models.CharField(max_length=255)  
    description = models.TextField()  
    duration_minutes = models.PositiveIntegerField()  
    min_age = models.PositiveIntegerField()  
    max_age = models.PositiveIntegerField() 

    def __str__(self):
        return self.name
    
class Schedule(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)  
    start_time = models.DateTimeField() 
    end_time = models.DateTimeField() 
    total_slots = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.section.name} | {self.start_time}"

class Booking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
     ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    client = models.OneToOneField('users.Client', on_delete=models.CASCADE,null=True, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)  
    parent_name = models.CharField(max_length=255) 
    parent_phone = models.CharField(max_length=20)  
    child_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)  
    confirmed_at = models.DateTimeField(null=True, blank=True) 
    cancelled_at = models.DateTimeField(null=True, blank=True) 
    def __str__(self):
        return f"{self.child_name} | {self.schedule.section.name} | {self.status}"

