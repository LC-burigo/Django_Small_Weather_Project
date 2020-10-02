from django.forms import ModelForm, TextInput
from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['Address', 'Dt']
        widgets = {'Address': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),
                   'Dt': TextInput(attrs={'class': 'input', 'placeholder': 'TimeStamp'})
                }