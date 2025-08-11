from django.forms import ModelForm
from dal import autocomplete
from django import forms
from .models import Servicio, MovimientoStock #,ServicioDetalle,DescripcionServicio

class ServicioForm(ModelForm):
    class Meta:
        model = Servicio
        fields = ['vehiculo', 'persona', 'tecnico', 'kilometraje_ant' ,'kilometraje_act', 'estado', 'kilometraje_diff', 'tipo','descripcion', 'fecha_fin']

        widgets = {
            'vehiculo':autocomplete.ModelSelect2(url='vehiculo-autocomplete', attrs={'class': 'form-control  mb-4 mt-1'}),
            'persona':autocomplete.ModelSelect2(url='persona-autocomplete',attrs={'class': 'form-control mb-4 mt-1'}),
            'tecnico':autocomplete.ModelSelect2(url='tecnico-autocomplete',attrs={'class': 'form-control  mb-4 mt-1', 'readonly': True}),
            'kilometraje_ant':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'id':'id_kilometraje_vehiculo', 'type':"hidden",  'name':"kilometraje_vehiculo"}),
            'kilometraje_act':forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1'}),
            'kilometraje_diff': forms.NumberInput(attrs={'class': 'form-control mb-4 mt-1', 'readonly': True}),
            'tipo' : forms.Select(attrs={'class': 'form-control mb-4 mt-1'}),
            'descripcion':forms.Textarea(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'Escribe la observación', 'rows':3}),
            'fecha_fin':forms.DateInput(attrs={'class': 'form-control mb-4 mt-1', 'placeholder': 'La fecha fin se llena al finalizar el servicio'}),
            'estado': forms.Select(attrs={'class': 'form-control mb-4 mt-1'})

        }
        labels = {
            'vehiculo': 'Vehículo',
            'descripcion': 'Descripción del Servicio',
            'kilometraje_ant': 'Kilometraje anterior',
            'kilometraje_act': 'Kilometraje al Finalizar',
            'kilometraje_diff': 'Diferencia de Kilometraje',
            'tipo': 'Tipo de Mantenimiento',
            'persona': 'Solicitante',
            'tecnico': 'Técnico Asignado',
            'fecha_fin': 'Fecha fin'
        }

    def clean_kilometraje_diff(self):
        kilometraje_diff = self.cleaned_data.get('kilometraje_diff')
        if kilometraje_diff is not None and kilometraje_diff < 0:
            raise forms.ValidationError("La diferencia de kilometraje no puede ser negativa.")
        return kilometraje_diff

    def clean(self):
        cleaned_data = super().clean()
        kilometraje_actual = cleaned_data.get('kilometraje_act')
        vehiculo = cleaned_data.get('vehiculo')
        
        if self.instance.pk:  # Es edición
            return cleaned_data
    
        if vehiculo and kilometraje_actual is not None:
            
            if kilometraje_actual < vehiculo.kilometraje:
                self.add_error('kilometraje_act', "El kilometraje actual no puede ser menor que el kilometraje registrado del vehículo.")
        return cleaned_data


class MovimientoStockForm(forms.ModelForm):
    class Meta:
        model = MovimientoStock
        fields = ['pieza', 'cantidad']
        widgets = {
            'pieza': autocomplete.ModelSelect2(url='pieza-autocomplete', attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pieza = cleaned_data.get('pieza')
        cantidad = cleaned_data.get('cantidad')
        if pieza and cantidad:
            if cantidad > pieza.cantidad_stock:
                raise forms.ValidationError(f"No hay suficiente stock para la pieza {pieza.nombre}. Stock disponible: {pieza.cantidad_stock}")
        return cleaned_data


# --- Formulario para cada detalle de servicio ---
# class ServicioDetalleForm(forms.ModelForm):
#     # Campo para la descripción del servicio, que permitirá autocompletar o crear
#     # Usaremos un CharField simple aquí y la lógica de autocompletar/crear será JS + AJAX
#     descripcion_texto = forms.CharField(
#         max_length=255,
#         required=False, # Puede ser requerido por JS si no se selecciona uno existente
#         label="Descripción del Servicio",
#         widget=forms.TextInput(attrs={
#             'class': 'form-control descripcion-servicio-input',
#             'placeholder': 'Escribe o selecciona una descripción...',
#             'data-descripcion-id': '' # Para guardar el ID de la descripción seleccionada
#         })
#     )

#     class Meta:
#         model = ServicioDetalle
#         fields = ['descripcion_servicio'] # Solo el ForeignKey al modelo DescripcionServicio
#         widgets = {
#             # Este campo estará oculto, su valor se llenará con JS
#             'descripcion_servicio': forms.HiddenInput(), 
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Si el formulario ya tiene una instancia (en edición), pre-llenar el campo de texto
#         if self.instance and self.instance.descripcion_servicio:
#             self.fields['descripcion_texto'].initial = self.instance.descripcion_servicio.descripcion
#             self.fields['descripcion_texto'].widget.attrs['data-descripcion-id'] = self.instance.descripcion_servicio.id

#     def clean(self):
#         cleaned_data = super().clean()
#         descripcion_texto = cleaned_data.get('descripcion_texto')
#         descripcion_servicio_obj = cleaned_data.get('descripcion_servicio')

#         # Lógica para "auto-registrar" o seleccionar existente
#         if descripcion_texto:
#             try:
#                 # Intenta encontrar una descripción existente
#                 descripcion_servicio_obj, created = DescripcionServicio.objects.get_or_create(
#                     descripcion__iexact=descripcion_texto, # Búsqueda insensible a mayúsculas/minúsculas
#                     defaults={'descripcion': descripcion_texto}
#                 )
#                 cleaned_data['descripcion_servicio'] = descripcion_servicio_obj
#             except DescripcionServicio.MultipleObjectsReturned:
#                 # Esto no debería pasar con unique=True, pero es buena práctica
#                 raise forms.ValidationError("Múltiples descripciones encontradas. Contacte al administrador.")
#         elif not descripcion_servicio_obj:
#             # Si no hay texto y no se seleccionó un objeto (ej. campo vacío)
#             raise forms.ValidationError("Debe proporcionar una descripción del servicio.")
        
#         return cleaned_data