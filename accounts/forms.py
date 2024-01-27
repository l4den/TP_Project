from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password.',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password.'
    }))

    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'last_name', 'phone_number', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name.'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name.'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username.'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number. eg. +38970123456'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address.'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if username is None or username == '':
            self.add_error('username', "Please enter a username.")

        if email is not None and email != '':
            if Account.objects.filter(email=email).exists():
                self.add_error('email', "An account with that email already exists.")

        if password is not None and password != '' and confirm_password is not None and confirm_password != '':
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")


class LoginForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address.'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password.'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
