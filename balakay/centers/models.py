from django.db import models
from django.contrib.auth.models import User
from users.models import Client, Child
from django.apps import apps
from django.utils import timezone
from datetime import timedelta
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)  #
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name
    
class Center(models.Model):
    partner = models.ForeignKey(
        'merchant.Partner',  # Используем строку вместо прямого импорта
        on_delete=models.CASCADE,
        related_name="centers",
        null=True,
        blank=True
    )
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
    EXPIRED = 'expired'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),  
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    client = models.OneToOneField('users.Client', on_delete=models.CASCADE, null=True, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)  
    parent_name = models.CharField(max_length=255) 
    parent_phone = models.CharField(max_length=20)  
    child_name = models.CharField(max_length=255)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.child_name} | {self.schedule.section.name} | {self.status}"
    
    def total_bookings_last_30_days(self):
        """Calculate the total bookings for the user in the last 30 days."""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        return Booking.objects.filter(
            user=self.user,
            created_at__gte=thirty_days_ago,
            status__in=[self.PENDING, self.CONFIRMED]
        ).count()
    
    def is_expired(self):
        """Check if the booking schedule time has passed."""
        return timezone.now() > self.schedule.start_time
    
    def update_status_if_expired(self):
        """Automatically mark the booking as expired if the schedule time has passed and still pending."""
        if self.status == self.PENDING and self.is_expired():
            self.status = self.EXPIRED
            self.save()



class FavoriteSection(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE) 
    section = models.ForeignKey(Section, on_delete=models.CASCADE) 
    added_at = models.DateTimeField(auto_now_add=True)  

    class Meta:
        unique_together = ('client', 'section')  

    def __str__(self):
        return f"{self.client.user.username} | {self.section.name}"
