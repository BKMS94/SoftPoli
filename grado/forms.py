from django.forms import ModelForm
from django import forms
from .models import Grado

class GradosForm(ModelForm):
    class Meta:
        model = Grado
        fields = ['orden', 'nombre', 'abreviatura']
        widgets = {
            'nombre': forms.TextInput(attrs = {'class':'form-control my-4', 'placeholder': 'Ingrese el nombre del grado'}),
            'abreviatura':  forms.TextInput( attrs= {'class': 'form-control my-4', 'placeholder': 'Ingrese la abreviatura del grado'}),
            'orden': forms.TextInput( attrs= {'class': 'form-control my-4', 'placeholder': 'Ingrese el orden Jerárquico del grado'})
        }