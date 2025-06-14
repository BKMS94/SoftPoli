from django.forms import ModelForm
from django import forms
from .models import Vehiculo

class VehiculoForm(ModelForm):

    class Meta:
          model = Vehiculo
          fields = ['placa', 'marca', 'modelo', 'anio', 'kilometraje',]

          labels = {'anio':'Año'}

          widgets = {'placa':forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la PLaca'}),
                     'marca':forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la Marca'}),
                     'modelo':forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el Modelo'}),
                     'anio':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el Año'}),
                     'kilometraje':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el kilometraje'}),
                     }