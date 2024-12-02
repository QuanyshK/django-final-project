from django import forms
from django.contrib.auth.models import User
from centers.models import Schedule, Center

class PartnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    center = forms.ModelChoiceField(queryset=Center.objects.all(), required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data



class ScheduleForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],  # Формат ISO 8601
        label="Start Time",
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'],  # Формат ISO 8601
        label="End Time",
    )

    class Meta:
        model = Schedule
        fields = ['section', 'start_time', 'end_time', 'total_slots']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'total_slots': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'section': 'Section',
            'total_slots': 'Total Slots',
        }

    def __init__(self, *args, **kwargs):
        sections_queryset = kwargs.pop('sections_queryset', None)
        super().__init__(*args, **kwargs)
        if sections_queryset:
            self.fields['section'].queryset = sections_queryset

    def clean(self):
        """
        Оставлена только базовая проверка времени начала и конца.
        """
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Start time must be earlier than end time.")

        return cleaned_data