from django.forms import ModelForm
from django import forms
from dal import autocomplete
from .models import Unidad, SubUnidad

class UnidadForm(ModelForm):
    class Meta:
        model = Unidad
        fields = ['nombre']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control my-4', 'placeholder': 'Ingrese el nombre de la comisaría'}),
        }

class SubunidadForm(ModelForm):
    class Meta:
        model = SubUnidad
        fields = ['nombre', 'direccion', 'telefono_contacto', 'responsable','unidad']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control my-4', 'placeholder': 'Ingrese el nombre de la comisaría'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control my-4', 'placeholder': 'Ingresa la dirección'}),
            'telefono_contacto': forms.NumberInput(attrs={'class':'form-control my-4', 'placeholder': 'Ingrese el teléfono del encargado'}), 
            'responsable': autocomplete.ModelSelect2(url='persona-autocomplete', attrs={'class': 'form-control  mb-4 mt-1'}),
            'unidad': autocomplete.ModelSelect2(url='unidad-autocomplete', attrs={'class': 'form-control  mb-4 mt-1'} )
        }