from django.forms import ModelForm
from dal import autocomplete
from django import forms
from .models import Servicio, MovimientoStock

class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'persona', 'tecnico', 'kilometraje_act', 'kilometraje_diff', 'descripcion']

        widgets = {
            'vehiculo':autocomplete.ModelSelect2(url='vehiculo-autocomplete', attrs={'class': 'form-control  mb-4 mt-1'}),
            'persona':autocomplete.ModelSelect2(url='persona-autocomplete',attrs={'class': 'form-control mb-4 mt-1'}),
            'tecnico':autocomplete.ModelSelect2(url='tecnico-autocomplete',attrs={'class': 'form-control  mb-4 mt-1', 'readonly': True}),
            'kilometraje_act':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1'}),
            'kilometraje_diff': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'readonly': True}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la observación', 'rows':3}),

        }


class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['pieza', 'cantidad']
        widgets = {
            'pieza': autocomplete.ModelSelect2(url='pieza-autocomplete', attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pieza = cleaned_data.get('pieza')
        cantidad = cleaned_data.get('cantidad')
        if pieza and cantidad:
            if cantidad > pieza.cantidad_stock:
                raise forms.ValidationError(f"No hay suficiente stock para la pieza {pieza.nombre}. Stock disponible: {pieza.cantidad_stock}")
        return cleaned_data
