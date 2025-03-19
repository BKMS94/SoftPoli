from django.forms import ModelForm
from .models import Pieza

class PiezaForm(ModelForm):
    class Meta :
        model = Pieza
        fields = ['nombre', 'cantidad_stock', 'reorder',]

