from django import forms
from .models import Persona, Tecnico

class TelefonoCleanMixin:
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        if len(telefono) < 7 or len(telefono) > 12:
            raise forms.ValidationError("El teléfono debe tener entre 7 y 12 dígitos.")
        return telefono

class PersonaForm(forms.ModelForm, TelefonoCleanMixin):
    class Meta:
        model = Persona
        fields = ['codigo', 'nombre', 'grado', 'telefono']
        labels = {
            'codigo': 'Código',
            'telefono': 'Teléfono',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el código'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el nombre'}),
            'grado': forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el teléfono'}),
        }

class TecnicoForm(forms.ModelForm, TelefonoCleanMixin):
    class Meta:
        model = Tecnico
        fields = ['codigo', 'nombre', 'grado', 'telefono']
        labels = {
            'codigo': 'Código',
            'telefono': 'Teléfono',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el código'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el nombre'}),
            'grado': forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe el teléfono'}),
        }


