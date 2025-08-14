from django import forms
from django.forms import inlineformset_factory
from dal import autocomplete
# Importa los modelos locales y los de otras apps
from .models import Requerimiento, RequerimientoDescripcionDetalle, RequerimientoPiezaDetalle, DescripcionServicio # ¡Importado DescripcionServicio localmente!
from vehiculo.models import Vehiculo
from ubicacion.models import Unidad # Asegúrate de importar Unidad
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
            'vehiculo':autocomplete.ModelSelect2(url='vehiculo-autocomplete',attrs={'class': 'form-select'}),
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
    # Campo de texto visible para el usuario, que se autocompletará/creará
    descripcion_texto = forms.CharField(
        max_length=255, # Usamos max_length para el CharField visible
        required=True,
        label="Descripción del Servicio",
        widget=forms.TextInput(attrs={
            'class': 'form-control descripcion-servicio-input',
            'placeholder': 'Escribe o selecciona una descripción...',
            'data-descripcion-id': '' # Para guardar el ID de la descripción seleccionada por JS
        })
    )


    class Meta:
        model = RequerimientoDescripcionDetalle
        # ¡CORREGIDO!: El campo del modelo para el FK es 'detalle'
        fields = ['detalle',] # Asegúrate que 'observaciones' esté en tu modelo RequerimientoDescripcionDetalle
        widgets = {
            # Este campo es el ForeignKey real, se llena con JS y se mantiene oculto
            'detalle': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.detalle:
            self.fields['descripcion_texto'].initial = self.instance.detalle.descripcion_servicio # Accede al campo de texto del modelo DescripcionServicio
            self.fields['descripcion_texto'].widget.attrs['data-descripcion-id'] = self.instance.detalle.id

    def clean(self):
        cleaned_data = super().clean()
        descripcion_texto = cleaned_data.get('descripcion_texto')
        
        if not descripcion_texto:
            self.add_error('descripcion_texto', "Debe proporcionar una descripción del servicio.")
            # Si no hay texto, no intentar buscar/crear DescripcionServicio
            return cleaned_data 

        try:
            # ¡CORREGIDO!: Usar el modelo DescripcionServicio LOCAL de esta misma app
            descripcion_servicio_obj, created = DescripcionServicio.objects.get_or_create(
                descripcion_servicio__iexact=descripcion_texto, # Usar el nombre del campo en DescripcionServicio (descripcion_servicio)
                defaults={'descripcion_servicio': descripcion_texto}
            )
            cleaned_data['detalle'] = descripcion_servicio_obj 
        except DescripcionServicio.MultipleObjectsReturned:
            self.add_error('descripcion_texto', "Múltiples descripciones encontradas. Contacte al administrador.")
            
        return cleaned_data



# --- Formulario y Formset para los Detalles de Piezas Propuestas ---
class RequerimientoPiezaDetalleForm(forms.ModelForm):
    class Meta:
        model = RequerimientoPiezaDetalle
        fields = ['pieza', 'cantidad']
        widgets = {
            'pieza': autocomplete.ModelSelect2(url='pieza-autocomplete', attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Cantidad'}),
        }
        labels = {
            'pieza': 'Pieza',
            'cantidad': 'Cantidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pieza'].queryset = Pieza.objects.all().order_by('nombre')

