from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, datetime, date
from .models import Booking
from users.models import Child

class BookingForm(forms.ModelForm):
    child = forms.ModelChoiceField(queryset=Child.objects.none(), required=True)

    class Meta:
        model = Booking
        fields = ['parent_name', 'parent_phone', 'child'] 

    def __init__(self, *args, section=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section  
        self.user = user 

        if self.user and hasattr(self.user, 'client'):
            active_children = Child.objects.filter(
                parent=self.user.client,
                usersubscription__is_active=True
            ).distinct()
            self.fields['child'].queryset = active_children
            self.fields['parent_name'].initial = self.user.client.first_name
            self.fields['parent_phone'].initial = self.user.client.phone_number

    def clean_child(self):
        child = self.cleaned_data.get('child')

        if not self.section:
            raise ValidationError("Section information is required for booking.")
        
        min_age = self.section.min_age 
        max_age = self.section.max_age

        if child:
            today = date.today()
            age = today.year - child.birth_date.year
            if (today.month, today.day) < (child.birth_date.month, child.birth_date.day):
                age -= 1  

            if age < min_age:
                raise ValidationError(f"{child.first_name} must be at least {min_age} years old to book this section.")
            elif age > max_age:
                raise ValidationError(f"{child.first_name} must be under {max_age} years old to book this section.")

            thirty_days_ago = today - timedelta(days=30)

            booking_count_monthly = Booking.objects.filter(
                child=child,
                created_at__gte=thirty_days_ago,
                status__in=[Booking.PENDING, Booking.CONFIRMED]
            ).count()

            if booking_count_monthly >= 30:
                raise ValidationError(f"{child.first_name} has reached the monthly booking limit of 30 visits.")

            today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))

            booking_count_daily = Booking.objects.filter(
                child=child,
                created_at__range=(today_start, today_end),
                status__in=[Booking.PENDING, Booking.CONFIRMED]
            ).count()

            if booking_count_daily >= 2:
                raise ValidationError(f"{child.first_name} has reached the daily booking limit of 2 visits.")

        return child
