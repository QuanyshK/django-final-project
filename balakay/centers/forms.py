from django import forms

from users.models import Child
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['parent_name', 'parent_phone'] 

    child = forms.ModelChoiceField(queryset=Child.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'client'):
            self.fields['child'].queryset = Child.objects.filter(parent=user.client)
