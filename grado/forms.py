from django.forms import ModelForm
from .models import Grado

class GradosForm(ModelForm):
    class Meta:
        model = Grado
        fields = ['nombre',]