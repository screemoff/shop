from django import forms
from . import models


class UserItem(forms.ModelForm):
    class Meta:
        model = models.UserItem
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={"placeholder": 'Price'}),
        }

class SearchForm(forms.ModelForm):
    class Meta:
        model = models.UserItem
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
        }
