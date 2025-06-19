from django.forms import ModelForm
from django import forms    
from .models import Pieza

class PiezaForm(ModelForm):
    class Meta:
        model = Pieza
        fields = ['nombre', 'cantidad_stock', 'reorder']
        labels = {
            'reorder': 'Cantidad de aviso'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el nombre'}),
            'cantidad_stock': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la cantidad'}),
            'reorder': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la cantidad'}),
        }

    def clean_cantidad_stock(self):
        cantidad = self.cleaned_data['cantidad_stock']
        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad

    def clean_reorder(self):
        reorder = self.cleaned_data['reorder']
        if reorder < 0:
            raise forms.ValidationError("La cantidad de aviso no puede ser negativa.")
        return reorder

