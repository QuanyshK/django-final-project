from django.contrib import admin
from .models import Partner

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "phone_number", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "contact_email", "phone_number")
    actions = ["activate_partners"]

    @admin.action(description="Активировать выбранных партнеров")
    def activate_partners(self, request, queryset):
        queryset.update(is_active=True)
