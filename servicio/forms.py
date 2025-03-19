from django.forms import ModelForm
from .models import Servicio, MovimientoStock

class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'persona', 'tecnico', 'kilometraje_act', 'kilometraje_diff', 'descripcion', 'costo']

class MovimientoStockForm(ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['pieza', 'servicio', 'cantidad']