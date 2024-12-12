from django.contrib import admin
from .models import Notification
# Register your models here.
@admin.register(Notification)

class Notification(admin.ModelAdmin):
    list_display = ('id', 'user', 'booking', 'created_at')
    search_fields = ('user',)
    ordering = ('id',)

