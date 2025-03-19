from django.forms import ModelForm
from .models import Vehiculo

class VehiculoForm(ModelForm):

    class Meta:
          model = Vehiculo
          fields = ['placa', 'marca', 'modelo', 'anio', 'kilometraje',]

          labels = {'anio':'Año'}