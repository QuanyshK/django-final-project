from django.contrib import admin
from .models import AgeGroup, Subscription


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'age_range', 'description')
    search_fields = ('age_range', 'description')
    ordering = ('id',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active', 'price', 'duration_text', 'age_group', 'total_days', 'freeze_days', 'daily_visits', 'monthly_visits', 'premium_monthly_visits')
    search_fields = ('name', 'age_group__age_range')
    list_filter = ('active', 'age_group')
    ordering = ('id',)
