from django.forms import ModelForm
from dal import autocomplete
from django import forms
from .models import Servicio, MovimientoStock

class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'persona', 'tecnico', 'kilometraje_ant' ,'kilometraje_act', 'kilometraje_diff', 'tipo','descripcion']

        widgets = {
            'vehiculo':autocomplete.ModelSelect2(url='vehiculo-autocomplete', attrs={'class': 'form-control  mb-4 mt-1'}),
            'persona':autocomplete.ModelSelect2(url='persona-autocomplete',attrs={'class': 'form-control mb-4 mt-1'}),
            'tecnico':autocomplete.ModelSelect2(url='tecnico-autocomplete',attrs={'class': 'form-control  mb-4 mt-1', 'readonly': True}),
            'kilometraje_ant':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'id':'id_kilometraje_vehiculo', 'type':"hidden",  'name':"kilometraje_vehiculo"}),
            'kilometraje_act':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1'}),
            'kilometraje_diff': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'readonly': True}),
            'tipo' : forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la observación', 'rows':3}),

        }
        labels = {
            'vehiculo': 'Vehículo',
            'descripcion': 'Descripción del Servicio',
            'kilometraje_ant': 'Kilometraje anterior',
            'kilometraje_act': 'Kilometraje al Finalizar',
            'kilometraje_diff': 'Diferencia de Kilometraje',
            'tipo': 'Tipo de Mantenimiento',
            'persona': 'Solicitante',
            'tecnico': 'Técnico Asignado',
        }

    def clean_kilometraje_diff(self):
        kilometraje_diff = self.cleaned_data.get('kilometraje_diff')
        if kilometraje_diff is not None and kilometraje_diff < 0:
            raise forms.ValidationError("La diferencia de kilometraje no puede ser negativa.")
        return kilometraje_diff

    def clean(self):
        cleaned_data = super().clean()
        kilometraje_actual = cleaned_data.get('kilometraje_act')
        vehiculo = cleaned_data.get('vehiculo')

        if vehiculo and kilometraje_actual is not None:
            # Asumiendo que Vehiculo tiene un campo 'kilometraje' que se actualiza
            if kilometraje_actual < vehiculo.kilometraje:
                self.add_error('kilometraje_act', "El kilometraje actual no puede ser menor que el kilometraje registrado del vehículo.")
        return cleaned_data


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
