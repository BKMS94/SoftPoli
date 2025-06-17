from django.forms import ModelForm,inlineformset_factory
from dal import autocomplete
from django import forms
from .models import Servicio, MovimientoStock,Pieza,Vehiculo,Tecnico

class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'persona', 'tecnico', 'kilometraje_act', 'kilometraje_diff', 'descripcion']

        widgets = {
            'vehiculo':autocomplete.ModelSelect2(url='vehiculo-autocomplete', attrs={'class': 'form-control mb-4 mt-1'}),
            'persona':autocomplete.ModelSelect2(url='persona-autocomplete',attrs={'class': 'form-control mb-4 mt-1'}),
            'tecnico':autocomplete.ModelSelect2(url='tecnico-autocomplete',attrs={'class': 'form-control mb-4 mt-1', 'readonly': True}),
            'kilometraje_act':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1'}),
            'kilometraje_diff': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'readonly': True}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la observación', 'rows':3}),

        }


class MovimientoStockForm(ModelForm):
    """
    Formulario para un solo item de pieza usada en el servicio.
    """
    class Meta:
        model = MovimientoStock
        fields = ['pieza', 'cantidad'] # Solo pieza y cantidad
        widgets = {
            'pieza': autocomplete.ModelSelect2(url='pieza-autocomplete',attrs={'class': 'form-control pieza-select mb-2'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input mb-2', 'min': '1'}), # Cantidad mínima 1
        }
        labels = {
            'pieza': 'Pieza',
            'cantidad': 'Cantidad',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puedes filtrar las piezas disponibles aquí si es necesario
        self.fields['pieza'].queryset = Pieza.objects.all().order_by('nombre')


# Crea un formset para MovimientoStock relacionados con un Servicio.
MovimientoStockFormSet = inlineformset_factory(
    Servicio,                 # Modelo padre
    MovimientoStock,          # Modelo hijo
    form=MovimientoStockForm, # Formulario para el hijo
    extra=1,                  # Número de formularios vacíos a mostrar inicialmente
    can_delete=True,          # Permite eliminar formularios existentes
    fields=['pieza', 'cantidad'] # Solo pieza y cantidad
)
