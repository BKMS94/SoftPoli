from django import forms
from dal import autocomplete
from .models import Requerimiento, RequerimientoDescripcionDetalle, RequerimientoPiezaDetalle 
from vehiculo.models import Vehiculo
from pieza.models import Pieza


# --- Formulario Principal para Requerimiento ---
class RequerimientoForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = [
            'vehiculo',
            'informe_tecnico_nro',
        ]
        widgets = {
            'vehiculo':autocomplete.ModelSelect2(url='vehiculo-autocomplete',attrs={'class': 'form-control'}),
            'informe_tecnico_nro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 529-04-2025'}),
        }
        labels = {
            'vehiculo': 'Vehículo',
            'informe_tecnico_nro': 'Nº Informe Técnico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.all().order_by('placa_int')


# --- Formulario y Formset para los Detalles de Servicios Propuestos ---
class RequerimientoDescripcionDetalleForm(forms.ModelForm):
    class Meta:
        model = RequerimientoDescripcionDetalle
        fields = ['descripcion_propuesta',] # Ahora solo gestiona el campo de texto directamente
        widgets = {
            'descripcion_propuesta': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe la descripción del servicio propuesto...',
                'rows': 2
            }),
        }
        labels = {
            'descripcion_propuesta': 'Descripción del Servicio',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ya no se necesita Select2 ni lógica de data-id para este campo.

    def clean(self):
        cleaned_data = super().clean()
        # La validación 'required' ya la maneja el modelo si blank=False
        return cleaned_data


# --- Formulario y Formset para los Detalles de Piezas Propuestas ---
class RequerimientoPiezaDetalleForm(forms.ModelForm):
    class Meta:
        model = RequerimientoPiezaDetalle
        fields = ['pieza', 'cantidad']
        widgets = {
            'pieza': autocomplete.ModelSelect2(url='pieza-autocomplete', attrs={'class': 'form-control'}), # Usar Select2 para Piezas
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Cantidad'}),
        }
        labels = {
            'pieza': 'Pieza',
            'cantidad': 'Cantidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pieza'].queryset = Pieza.objects.all().order_by('nombre')
