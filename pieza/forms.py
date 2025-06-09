from django.forms import ModelForm
from django import forms    
from .models import Pieza

class PiezaForm(ModelForm):
    class Meta :
        model = Pieza
        fields = ['nombre', 'cantidad_stock', 'reorder',]
        labels = {
            'reorder':'Cantidad de aviso'
        }
        widgets = {
            'nombre':forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el nombre'}),
            'cantidad_stock':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la cantidad'}),
            'reorder':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el cantidad'}),

        }

