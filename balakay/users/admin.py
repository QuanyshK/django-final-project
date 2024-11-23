from django.contrib import admin
from .models import Client, Child, UserSubscription


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'city', 'user')
    search_fields = ('first_name', 'last_name', 'phone_number', 'city')
    list_filter = ('city',)
    ordering = ('id',)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birth_date', 'gender', 'parent')
    search_fields = ('first_name', 'last_name', 'parent__first_name', 'parent__last_name')
    list_filter = ('gender',)
    ordering = ('id',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'child', 'subscription_type', 'is_active', 'activation_date', 'expiration_date', 'total_days', 'used_visits', 'total_visits')
    search_fields = ('parent__first_name', 'parent__last_name', 'child__first_name', 'child__last_name', 'subscription_type__name')
    list_filter = ('is_active', 'subscription_type')
    ordering = ('id',)
