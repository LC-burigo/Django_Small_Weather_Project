from django import forms
from django.forms import ModelForm, TextInput
from .models import City


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['Address', 'Dt']
        widgets = {'Address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City Name'}),
                   'Dt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TimeStamp'}),
                }