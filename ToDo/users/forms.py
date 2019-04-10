from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email

User = get_user_model()



class LoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.EmailInput(attrs = {'placeholder': 'Login with email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Type current password'}))

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Such user doesn\'t exists.')

        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise forms.ValidationError('Incorrect password')



class RegistrationForm(forms.ModelForm):

    username = forms.CharField(label='', widget=forms.TextInput(attrs = {'placeholder': 'Type your username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Type new password'}))
    password_check = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm password above'}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs = {'placeholder': 'Type your email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']


        if '@' not in email:
            raise forms.ValidationError('Missing @ sign in email.')
        if '.' not in email:
            raise forms.ValidationError('Missing . sign in email.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('You cannot use this email.')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('User with such name already exists.')
        if password != password_check:
            raise forms.ValidationError('Your passwords don\'t match')

        try:
            mt = validate_email(email)
        except:
            raise forms.ValidationError('Incorrect email.')
