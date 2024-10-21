from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Client



class ClientRegistrationForm(forms.ModelForm):
    # This form will also handle User model creation for authentication
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'phone_number', 'city']

    def save(self, commit=True):
        # Save the User part first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        client = super(ClientRegistrationForm, self).save(commit=False)
        client.user = user  # Link the newly created User to the Client
        if commit:
            client.save()
        return client


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))