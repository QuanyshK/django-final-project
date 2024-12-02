from django import forms
from django.contrib.auth.models import User
from centers.models import Schedule, Center

class PartnerRegistrationForm(forms.ModelForm):
    # Fields for password input
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    # Dropdown for selecting a center, required for partners
    center = forms.ModelChoiceField(queryset=Center.objects.all(), required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            # Raise a validation error if passwords do not match
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['section', 'start_time', 'end_time', 'total_slots']

