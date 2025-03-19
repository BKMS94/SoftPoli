from django.forms import ModelForm
from .models import Persona, Tecnico

class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = ['codigo', 'nombre', 'grado', 'telefono', ]
        
        labels = {
            'codigo': 'Código',
            'telefono': 'Teléfono',
        }
        
class TecnicoForm(ModelForm):
    class Meta:
        model = Tecnico
        fields = ['codigo', 'nombre', 'grado', 'telefono', ]
        
        labels = {
            'codigo': 'Código',
            'telefono': 'Teléfono',
        }
        

