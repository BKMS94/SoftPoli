from django.forms import ModelForm
from django import forms
from .models import Grado

class GradosForm(ModelForm):
    class Meta:
        model = Grado
        fields = ['nombre',]
        widgets = {
            'nombre': forms.TextInput(attrs = {'class':'form-control my-4', 'placeholder': 'Ingrese el nombre del grado',
                })
        }