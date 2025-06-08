from django.forms import ModelForm
from django import forms
from .models import Persona, Tecnico

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['codigo', 'nombre', 'grado', 'telefono', ]
        
        labels = {
            'codigo': 'Código',
            'telefono': 'Teléfono',
        }

        widgets = {
            'codigo':forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe tu código'}),
            'nombre':forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe tu nombre'}),
            'grado':forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'telefono':forms.TextInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe tu teléfono'}),
        }
        
class TecnicoForm(ModelForm):
    class Meta:
        model = Tecnico
        fields = ['codigo', 'nombre', 'grado', 'telefono', ]
        
        labels = {
            'codigo': 'Código',
            'telefono': 'Teléfono',
        }
        

