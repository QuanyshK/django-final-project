from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['parent_name', 'parent_phone', 'child_name']
        widgets = {
            'parent_name': forms.TextInput(attrs={'placeholder': 'Parent Name'}),
            'parent_phone': forms.TextInput(attrs={'placeholder': 'Parent Phone'}),
            'child_name': forms.TextInput(attrs={'placeholder': 'Child Name'}),
        }
