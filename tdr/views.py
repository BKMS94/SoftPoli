from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone

# Para PDF (WeasyPrint)
from weasyprint import HTML

# Para Word (python-docx) - Comentado ya que no está implementado en este scope
# from docx import Document
from io import BytesIO

# Importa los modelos necesarios
from maestranza.utils import modo_gestion, paginacion
from .models import Requerimiento, RequerimientoDescripcionDetalle, RequerimientoPiezaDetalle, DescripcionServicio
from .forms import RequerimientoForm, RequerimientoPiezaDetalleForm, RequerimientoDescripcionDetalleForm
from vehiculo.models import Vehiculo
from ubicacion.models import SubUnidad # Necesario para Requerimiento.comisaria
from pieza.models import Pieza # Necesario para buscar_piezas_api

# Asumiendo que maestranza.utils existe y contiene paginacion y modo_gestion
# from maestranza.utils import paginacion,modo_gestion


# --- Vistas CRUD para Requerimientos (Funciones) ---

def lista_requerimientos(request):
    """
    Muestra una lista de todos los requerimientos (TDRs).
    Permite búsqueda por placa interna del vehículo.
    """
    search_query = request.GET.get('search', '')
    requerimientos = Requerimiento.objects.filter(
        Q(vehiculo__placa_int__icontains=search_query)
    ).order_by('-fecha_creacion')



    # Asumiendo que 'paginacion' es una función que maneja la paginación de QuerySets
    # Si no tienes esta utilidad, puedes usar Paginator de Django directamente.
    requerimientos = paginacion(request, requerimientos) 
    
    context = {
        'requerimientos': requerimientos,
        'urlindex': 'lista_requerimientos', 
        'urlcrear': 'crear_requerimiento', 
        'search_query': search_query
    }
    # La plantilla 'requerimiento/index.html' debería ser 'requerimientos/lista_requerimientos.html'
    # para consistencia, pero mantengo la que indicaste.
    return render(request, 'requerimiento/index.html', context)


def detalle_requerimiento(request, pk):
    """
    Muestra los detalles de un requerimiento específico,
    cargando las relaciones necesarias de forma eficiente.
    """
    requerimiento = get_object_or_404(Requerimiento.objects
                                 .select_related('vehiculo', 'comisaria') # Incluir comisaria
                                 .prefetch_related('requerimientodescripciondetalle_set__detalle', # Correcto: 'detalle' es el FK
                                                   'requerimientopiezadetalle_set__pieza'),
                                 pk=pk)
    context = {
        'requerimiento': requerimiento
    }
    return render(request, 'requerimientos/detalle_requerimiento.html', context) # Ajustado a requerimientos/detalle_requerimiento.html


def requerimiento_form(request, id=None):
    """
    Permite crear o editar un requerimiento (TDR) y sus detalles.
    """
    requerimiento, modo, extra = modo_gestion(Requerimiento,id)

    # Define los Formsets aquí, usando los formularios correctos
    RequerimientoDescripcionDetalleFormSet = inlineformset_factory(
        Requerimiento,
        RequerimientoDescripcionDetalle,
        form=RequerimientoDescripcionDetalleForm,
        extra=extra, # Usa la variable 'extra'
        can_delete=True,
        # 'detalle' es el ForeignKey, 'observaciones' es el TextField en RequerimientoDescripcionDetalle
        fields=['detalle'] 
    )

    RequerimientoPiezaDetalleFormSet = inlineformset_factory(
        Requerimiento,
        RequerimientoPiezaDetalle,
        form=RequerimientoPiezaDetalleForm,
        extra=extra, # Un formulario vacío por defecto al crear, 0 al editar
        can_delete=True,
        fields=['pieza', 'cantidad'],
    )

    if request.method == 'POST':
        form = RequerimientoForm(request.POST, instance=requerimiento)
        # Es CRUCIAL que los prefijos aquí ('serviciodetalle', 'piezadetalle')
        # coincidan con los usados en el template HTML para los formsets.
        servicio_detalle_formset = RequerimientoDescripcionDetalleFormSet(request.POST, instance=requerimiento, prefix='serviciodetalle')
        pieza_detalle_formset = RequerimientoPiezaDetalleFormSet(request.POST, instance=requerimiento, prefix='piezadetalle')
        
        if form.is_valid() and servicio_detalle_formset.is_valid() and pieza_detalle_formset.is_valid():
            with transaction.atomic():
                requerimiento = form.save() # Guarda el objeto Requerimiento principal

                servicio_detalle_formset.instance = requerimiento
                servicio_detalle_formset.save()

                pieza_detalle_formset.instance = requerimiento
                pieza_detalle_formset.save()
            
            messages.success(request, f'Requerimiento (TDR) {"creado" if modo == "crear" else "actualizado"} exitosamente.')
            return redirect('lista_requerimientos') # Redirige a la lista general
        else:
            messages.error(request, f'Error al {"crear" if modo == "crear" else "actualizar"} el requerimiento. Revise los campos.')
    else: # GET request
        form = RequerimientoForm(instance=requerimiento)
        servicio_detalle_formset = RequerimientoDescripcionDetalleFormSet(instance=requerimiento, prefix='serviciodetalle')
        pieza_detalle_formset = RequerimientoPiezaDetalleFormSet(instance=requerimiento, prefix='piezadetalle')
    
    context = {
        'form': form,
        'servicio_detalle_formset': servicio_detalle_formset,
        'pieza_detalle_formset': pieza_detalle_formset,
        'requerimiento': requerimiento, # Se pasa la instancia (o None) para el modo
        'modo': modo
    }
    # La plantilla 'requerimientos/gestion.html' es correcta aquí.
    return render(request, 'requerimiento/gestion.html', context)

def borrar_requerimiento(request, pk):
    """
    Permite eliminar un requerimiento (TDR).
    """
    requerimiento = get_object_or_404(Requerimiento, pk=pk)
    if request.method == 'POST':
        requerimiento.delete()
        messages.success(request, 'Requerimiento (TDR) eliminado exitosamente.')
        return redirect('lista_requerimientos') # Redirige a la lista general
    context = {
        'requerimiento': requerimiento
    }
    return render(request, 'requerimientos/requerimiento_confirm_delete.html', context)

# --- Vista para Generar Documento PDF del TDR ---

def generar_tdr_pdf(request, pk):
    """
    Genera el documento PDF "Términos de Referencia" para un requerimiento específico.
    """
    requerimiento = get_object_or_404(Requerimiento.objects
                                     .select_related('vehiculo', 'comisaria') # Incluir comisaria en select_related
                                     .prefetch_related('requerimientodescripciondetalle_set__detalle', # Correcto: 'detalle'
                                                       'requerimientopiezadetalle_set__pieza'),
                                     pk=pk)
    
    vehiculo = requerimiento.vehiculo
    comisaria_unidad = requerimiento.comisaria # Objeto Unidad

    # NOTA: Tu modelo 'Requerimiento' actual (según el forms.py) NO tiene los campos:
    # responsable_tdr, unidad_regpol, hora_inicio_trabajo, hora_fin_trabajo.
    # Por lo tanto, se usan placeholders o se asume que estos datos se obtendrán de otra parte.
    # Si estos campos son necesarios en el PDF, DEBERÍAN ser añadidos al modelo Requerimiento.
    
    context = {
        'requerimiento': requerimiento,
        'vehiculo': vehiculo,
        'comisaria_unidad': comisaria_unidad, # Pasamos el objeto Unidad de la comisaría
        
        # Placeholders o datos estáticos, ya que no están en el modelo Requerimiento actual:
        'persona': None, # Asumiendo un objeto Persona para el conductor/responsable si lo necesitas
        'tecnico': None, # Asumiendo un objeto Tecnico si lo necesitas
        'hora_inicio': 'HH:MM', # Placeholder
        'hora_fin': 'HH:MM', # Placeholder
        'unidad_regpol_doc': 'REGPOL - TRUJILLO', # Placeholder o un valor fijo
        
        # Datos que sí provienen del modelo Requerimiento:
        'informe_tecnico_nro_doc': requerimiento.informe_tecnico_nro or '__________',
        'comisaria_doc': requerimiento.comisaria.nombre if requerimiento.comisaria else '[COMISARÍA NO ESPECIFICADA]', # Nombre de la Unidad FK
        'fecha_actual': timezone.now(),
        'logo_url': request.build_absolute_uri('/static/img/sello-pnp.png'),
    }
    
    html_string = render_to_string(
        'requerimientos/tdr_vehiculo_pdf.html',
        context,
        request=request
    )
    
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="tdr_vehiculo_{requerimiento.id}.pdf"'
    return response

# --- Vistas API para AJAX (autocompletar descripciones de servicio y piezas) ---
# Estas vistas permanecen como funciones y son reutilizables.

def buscar_descripcion_servicio_api(request):
    """
    Vista API para buscar descripciones de servicio existentes (para Select2)
    desde el catálogo LOCAL de 'requerimientos'.
    """
    query = request.GET.get('q', '')
    if query:
        # Aquí usa el campo 'descripcion_servicio' del modelo DescripcionServicio local
        descripciones = DescripcionServicio.objects.filter(descripcion_servicio__icontains=query)[:10]
        results = [{'id': d.id, 'text': d.descripcion_servicio} for d in descripciones]
    else:
        results = []
    return JsonResponse({'results': results})

def crear_descripcion_servicio_api(request):
    """
    Vista API para crear una nueva descripción de servicio si no existe,
    en el catálogo LOCAL de 'requerimientos'.
    """
    if request.method == 'POST':
        descripcion_texto = request.POST.get('descripcion', '').strip()
        if descripcion_texto:
            try:
                # Aquí usa el campo 'descripcion_servicio' del modelo DescripcionServicio local
                descripcion_obj, created = DescripcionServicio.objects.get_or_create(
                    descripcion_servicio__iexact=descripcion_texto,
                    defaults={'descripcion_servicio': descripcion_texto}
                )
                return JsonResponse({'id': descripcion_obj.id, 'text': descripcion_obj.descripcion_servicio, 'created': created})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido o descripción vacía'}, status=400)

def buscar_piezas_api(request):
    """
    Vista API para buscar piezas existentes (para Select2).
    """
    query = request.GET.get('q', '')
    if query:
        piezas = Pieza.objects.filter(nombre__icontains=query)[:10]
        results = [{'id': p.id, 'text': f"{p.nombre} (Stock: {p.stock_actual})"} for p in piezas]
    else:
        results = []
    return JsonResponse({'results': results})
