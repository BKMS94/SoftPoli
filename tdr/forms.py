from django import forms
from django.forms import inlineformset_factory
from dal import autocomplete
# Importa los modelos locales y los de otras apps
from .models import Requerimiento, RequerimientoDescripcionDetalle, RequerimientoPiezaDetalle, DescripcionServicio # ¡Reintroducido DescripcionServicio!
from vehiculo.models import Vehiculo
from ubicacion.models import Unidad # Se mantiene si Unidad se usa en otros modelos
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
    # ¡NUEVO/REINTRODUCIDO!: Campo de texto visible para el usuario, que se autocompletará/creará
    descripcion_texto = forms.CharField(
        max_length=255,
        required=False, # Hacemos este campo no requerido a nivel de Django forms,
                         # la validación fuerte se hace en clean()
        label="Descripción del Servicio",
        widget=forms.TextInput(attrs={
            'class': 'form-control descripcion-servicio-input', # Clase para JS
            'placeholder': 'Escribe o selecciona una descripción...',
            'data-descripcion-id': '' # Para guardar el ID de la descripción seleccionada por JS
        })
    )

    class Meta:
        model = RequerimientoDescripcionDetalle
        # ¡CORREGIDO!: Ahora el campo es 'detalle' (ForeignKey)
        fields = ['detalle',]
        widgets = {
            # Este campo es el ForeignKey real que se guarda, se llena con JS y se mantiene oculto
            'detalle': forms.HiddenInput(),
        }
        labels = {
            'detalle': 'Descripción del Servicio', # Etiqueta para el campo subyacente
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-poblar descripcion_texto si ya existe un detalle asociado
        if self.instance and self.instance.detalle:
            self.fields['descripcion_texto'].initial = self.instance.detalle.descripcion_servicio
            self.fields['descripcion_texto'].widget.attrs['data-descripcion-id'] = self.instance.detalle.id
        else:
            # Si es un formulario vacío para una nueva fila, asegura que data-descripcion-id esté vacío
            self.fields['descripcion_texto'].widget.attrs['data-descripcion-id'] = ''


    def clean(self):
        cleaned_data = super().clean()
        descripcion_texto = cleaned_data.get('descripcion_texto')
        # Obtener el ID del detalle desde la data POST, que Select2 debería haber llenado en el HiddenInput
        detalle_fk_id = self.data.get(self.prefix + '-detalle') 
        
        # Validación: Si no hay texto de descripción y no hay un ID de detalle
        if not descripcion_texto and not detalle_fk_id:
            # Añadimos el error al campo visible para el usuario
            self.add_error('descripcion_texto', "Debe proporcionar una descripción del servicio.")
            # Es importante retornar aquí si no hay datos válidos para evitar errores subsiguientes
            # o intentar buscar un objeto no existente.
            return cleaned_data # Retorna los datos limpios hasta este punto

        # Si hay texto de descripción, intentar buscar/crear DescripcionServicio
        if descripcion_texto:
            try:
                # Usar el modelo DescripcionServicio para buscar/crear
                descripcion_obj, created = DescripcionServicio.objects.get_or_create(
                    descripcion_servicio__iexact=descripcion_texto, # Búsqueda insensible a mayúsculas/minúsculas
                    defaults={'descripcion_servicio': descripcion_texto}
                )
                cleaned_data['detalle'] = descripcion_obj # Asignar el objeto DescripcionServicio al ForeignKey
            except DescripcionServicio.MultipleObjectsReturned:
                self.add_error('descripcion_texto', "Múltiples descripciones encontradas. Contacte al administrador.")
            except Exception as e:
                self.add_error('descripcion_texto', f"Error al procesar la descripción: {e}")

        elif detalle_fk_id:
            # Si no hay descripcion_texto pero hay un detalle_fk_id (ej. un campo pre-cargado desde BD
            # o seleccionado de la lista existente por el usuario)
            try:
                cleaned_data['detalle'] = DescripcionServicio.objects.get(pk=detalle_fk_id)
            except DescripcionServicio.DoesNotExist:
                self.add_error('descripcion_texto', "La descripción del servicio seleccionada no es válida.")
            except Exception as e:
                self.add_error('descripcion_texto', f"Error al cargar la descripción seleccionada: {e}")
        else:
            # Si ninguna de las condiciones anteriores se cumple (ej. el campo se limpió)
            cleaned_data['detalle'] = None
            
        return cleaned_data


# --- Formulario y Formset para los Detalles de Piezas Propuestas ---
class RequerimientoPiezaDetalleForm(forms.ModelForm):
    class Meta:
        model = RequerimientoPiezaDetalle
        fields = ['pieza', 'cantidad']
        widgets = {
            'pieza': autocomplete.ModelSelect2(url='pieza-autocomplete', attrs={'class': 'form-select'}), # Usar Select2 para Piezas
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Cantidad'}),
        }
        labels = {
            'pieza': 'Pieza',
            'cantidad': 'Cantidad',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pieza'].queryset = Pieza.objects.all().order_by('nombre')
