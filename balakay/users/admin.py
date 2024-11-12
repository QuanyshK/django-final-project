from django.contrib import admin
from django import forms
from .models import Client, Child, UserSubscription


class UserSubscriptionForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Client.objects.filter(child__isnull=False).distinct()
        if 'parent' in self.data:
            try:
                parent_id = int(self.data.get('parent'))
                self.fields['child'].queryset = Child.objects.filter(parent_id=parent_id)
            except (ValueError, TypeError):
                self.fields['child'].queryset = Child.objects.none()
        elif self.instance.pk:
            self.fields['child'].queryset = Child.objects.filter(parent=self.instance.parent)
        else:
            self.fields['child'].queryset = Child.objects.none()

class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('child', 'parent', 'subscription_type', 'is_active', 'total_days', 'used_visits', 'expiration_date')
    readonly_fields = ('used_visits', 'expiration_date') 

    def save_model(self, request, obj, form, change):
        if not change:
            if not obj.total_days:
                obj.total_days = 30
            if not obj.total_visits:
                obj.total_visits = 30
            if not obj.daily_visits_limit:
                obj.daily_visits_limit = 2
        obj.save()

admin.site.register(Client)
admin.site.register(Child)
admin.site.register(UserSubscription, UserSubscriptionAdmin)
