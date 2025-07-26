from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'vin', 'marca', 'modelo', 'tipo', 'anio', 'tipo_combustible', 'kilometraje', 'estado','fecha_adquisicion']
        labels = {'anio': 'Año'}
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la Placa'}),
            'vin': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el VIN'}),
            'marca': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el Modelo'}),
            'tipo': forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el Año'}),
            'tipo_combustible': forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el kilometraje'}),
            'estado': forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'fecha_adquisicion': forms.DateTimeInput(attrs={'class': 'form-control mb-4 mt-1'}),

        }

    def clean_anio(self):
        anio = self.cleaned_data['anio']
        if anio < 1900 or anio > 2100:
            raise forms.ValidationError("El año debe estar entre 1900 y 2100.")
        return anio

    def clean_kilometraje(self):
        km = self.cleaned_data['kilometraje']
        if km < 0:
            raise forms.ValidationError("El kilometraje no puede ser negativo.")
        return km