from django.contrib import admin
from .models import Category, Center, Section, Schedule, Booking, FavoriteSection


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    ordering = ('id',)


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager_name', 'manager_phone', 'city', 'address')
    search_fields = ('name', 'manager_name', 'manager_phone', 'city', 'address')
    list_filter = ('city',)
    ordering = ('id',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'center', 'category', 'min_age', 'max_age', 'duration_minutes')
    search_fields = ('name', 'center__name', 'category__name')
    list_filter = ('center', 'category')
    ordering = ('id',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'start_time', 'end_time', 'total_slots')
    search_fields = ('section__name',)
    list_filter = ('start_time',)
    ordering = ('id',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'child_name', 'schedule', 'parent_name', 'parent_phone', 'status', 'created_at', 'confirmed_at', 'cancelled_at')
    search_fields = ('child_name', 'parent_name', 'parent_phone', 'schedule__section__name')
    list_filter = ('status', 'created_at')
    ordering = ('id',)


@admin.register(FavoriteSection)
class FavoriteSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'section', 'added_at')
    search_fields = ('client__user__username', 'section__name')
    ordering = ('id',)
