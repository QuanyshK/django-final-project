from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from users.models import Child, UserSubscription
from .models import Booking, Section

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
                raise ValidationError(f"Child must be at least {min_age} years old to book this section.")
            elif age > max_age:
                raise ValidationError(f"Child must be at under {max_age} years old to book this section.")

        return child
