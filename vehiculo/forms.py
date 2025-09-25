from django import forms
from .models import Vehiculo
from dal import  autocomplete

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa_int','placa_rod', 'vin', 'num_motor', 'marca', 'modelo', 'tipo', 'anio', 'tipo_combustible', 'procedencia',
                  'kilometraje', 'estado_vehi', 'estado_odo','funcion','fecha_adquisicion', 'subunidad','valor', 'motivo_ino', 'fecha_ino','ubicacion_ino','resolucion_baja','fecha_baja']
        labels = {'anio': 'Año', 'subunidad': 'Sub Unidad Asignada'}
        widgets = {
            'placa_int': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe la Placa'}),
            'placa_rod': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe la Placa'}),
            'vin': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe el VIN'}),
            'num_motor': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe el VIN'}),
            'marca': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe la Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe el Modelo'}),
            'tipo': forms.Select(attrs={'class': 'form-control mb-3 mt-1'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe el Año'}),
            'tipo_combustible': forms.Select(attrs={'class': 'form-control mb-3 mt-1'}),
            'procedencia': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe la procedencia'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe el kilometraje'}),
            'estado_vehi': forms.Select(attrs={'class': 'form-control mb-3 mt-1'}),
            'estado_odo': forms.Select(attrs={'class': 'form-control mb-3 mt-1'}),
            'funcion': forms.Select(attrs={'class': 'form-control mb-3 mt-1'}),            
            'fecha_adquisicion': forms.DateInput(
                attrs={'class': 'form-control mb-4 mt-1', 'type':'date', 'placeholder': 'Escoje la fecha de adquisición'},
                format='%Y-%m-%d'
            ),
            'subunidad': autocomplete.ModelSelect2(url='subunidad-autocomplete',attrs={'class': 'form-control mb-3 mt-1'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe el valor de adquisicion'}),
            'motivo_ino':forms.Textarea(attrs={'class': 'form-control-area mb-4 mt-1', 'placeholder': 'Escribe el motivo de inoperatividad', 'rows':3}),
            'fecha_ino': forms.DateInput(
                attrs={'class': 'form-control mb-4 mt-1', 'type':'date', 'placeholder': 'Escoje la fecha de inoperatividad'},
                format='%Y-%m-%d'
            ),
            'ubicacion_ino': autocomplete.ModelSelect2(url='subunidad-autocomplete',attrs={'class': 'form-control mb-3 mt-1'}),  
            'resolucion_baja': forms.TextInput(attrs={'class': 'form-control mb-3 mt-1', 'placeholder': 'Escribe la resolución de la baja'}),
            'fecha_baja': forms.DateInput(
                attrs={'class': 'form-control mb-4 mt-1', 'type':'date', 'placeholder': 'Escoje la fecha de baja'},
                format='%Y-%m-%d'
            ),         
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

class VehiculoImportForm(forms.Form):
    archivo = forms.FileField(label="Archivo Excel")