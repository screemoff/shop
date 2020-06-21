from django import forms
from .models import MessageModel

class AuthForm(forms.Form):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='Username')
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')


class RegisterForm(AuthForm):
    first_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    money = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Money'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))


class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageModel
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={'placeholder': 'Написать сообщение'})}