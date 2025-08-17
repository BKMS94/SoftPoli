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
from .models import Requerimiento, RequerimientoDescripcionDetalle, RequerimientoPiezaDetalle, DescripcionServicio # ¡Reintroducido DescripcionServicio!
from .forms import RequerimientoForm, RequerimientoPiezaDetalleForm, RequerimientoDescripcionDetalleForm
from vehiculo.models import Vehiculo
from ubicacion.models import Unidad # Necesario si Unidad se usa en otros modelos, pero ya no en Requerimiento directamente
from pieza.models import Pieza # Necesario para buscar_piezas_api


# --- Vistas CRUD para Requerimientos (Funciones) ---

def requerimiento_lista(request):
    search_query = request.GET.get('search', '')
    requerimientos = Requerimiento.objects.filter(
        Q(vehiculo__placa_int__icontains=search_query)
    ).order_by('-fecha_creacion')
    
    requerimientos = paginacion(request, requerimientos) 
    
    context = {
        'requerimientos': requerimientos,
        'urlindex': 'lista_requerimientos', 
        'urlcrear': 'crear_requerimiento', 
        'search_query': search_query
    }
    return render(request, 'requerimiento/index.html', context)


def detalle_requerimiento(request, id):
    requerimiento = get_object_or_404(Requerimiento.objects
                                 .select_related('vehiculo') 
                                 .prefetch_related('detalles_servicio__detalle', # ¡CORREGIDO!: Accede via .detalle
                                                   'detalles_pieza__pieza'),
                                 id=id)
    context = {
        'requerimiento': requerimiento
    }
    return render(request, 'requerimientos/detalle_requerimiento.html', context)


def requerimiento_form(request, id=None):
    requerimiento, modo, extra = modo_gestion(Requerimiento, id)

    RequerimientoDescripcionDetalleFormSet = inlineformset_factory(
        Requerimiento,
        RequerimientoDescripcionDetalle,
        form=RequerimientoDescripcionDetalleForm,
        extra=extra,
        can_delete=True,
        fields=['detalle'] # ¡CORREGIDO!: Ahora usa el ForeignKey 'detalle'
    )

    RequerimientoPiezaDetalleFormSet = inlineformset_factory(
        Requerimiento,
        RequerimientoPiezaDetalle,
        form=RequerimientoPiezaDetalleForm,
        extra=extra,
        can_delete=True,
        fields=['pieza', 'cantidad'],
    )

    if request.method == 'POST':
        form = RequerimientoForm(request.POST, instance=requerimiento)
        servicio_detalle_formset = RequerimientoDescripcionDetalleFormSet(request.POST, instance=requerimiento, prefix='serviciodetalle') # <<<< ASEGURA QUE ES 'serviciodetalle'
        pieza_detalle_formset = RequerimientoPiezaDetalleFormSet(request.POST, instance=requerimiento, prefix='piezadetalle') # <<<< ASEGURA QUE ES 'piezadetalle'
        
        if form.is_valid() and servicio_detalle_formset.is_valid() and pieza_detalle_formset.is_valid():
            with transaction.atomic():
                requerimiento = form.save() 

                servicio_detalle_formset.instance = requerimiento
                servicio_detalle_formset.save()

                pieza_detalle_formset.instance = requerimiento
                pieza_detalle_formset.save()
            
            messages.success(request, f'Requerimiento (TDR) {"creado" if modo == "crear" else "actualizado"} exitosamente.')
            return redirect('lista_requerimientos') 
        else:
            messages.error(request, f'Error al {"crear" if modo == "crear" else "actualizar"} el requerimiento. Revise los campos.')
    else: 
        form = RequerimientoForm(instance=requerimiento)
        servicio_detalle_formset = RequerimientoDescripcionDetalleFormSet(instance=requerimiento, prefix='serviciodetalle') # <<<< ASEGURA QUE ES 'serviciodetalle'
        pieza_detalle_formset = RequerimientoPiezaDetalleFormSet(instance=requerimiento, prefix='piezadetalle') # <<<< ASEGURA QUE ES 'piezadetalle'
    
    context = {
        'form': form,
        'servicio_detalle_formset': servicio_detalle_formset,
        'pieza_detalle_formset': pieza_detalle_formset,
        'requerimiento': requerimiento, 
        'modo': modo
    }
    return render(request, 'requerimiento/gestion.html', context)


def borrar_requerimiento(request, id):
    requerimiento = get_object_or_404(Requerimiento, id=id)
    if request.method == 'POST':
        requerimiento.delete()
        messages.success(request, 'Requerimiento (TDR) eliminado exitosamente.')
        return redirect('lista_requerimientos') 
    context = {
        'requerimiento': requerimiento
    }
    return render(request, 'requerimientos/requerimiento_confirm_delete.html', context)


def generar_tdr_pdf(request, id):
    requerimiento = get_object_or_404(Requerimiento.objects
                                     .select_related('vehiculo') 
                                     .prefetch_related('detalles_servicio__detalle', # ¡CORREGIDO!: Accede via .detalle
                                                       'detalles_pieza__pieza'),
                                     id=id)
    
    vehiculo = requerimiento.vehiculo

    context = {
        'requerimiento': requerimiento,
        'vehiculo': vehiculo,
        
        'persona': None, 
        'tecnico': None, 
        'hora_inicio': 'HH:MM', 
        'hora_fin': 'HH:MM', 
        'unidad_regpol_doc': 'REGPOL - TRUJILLO', 
        
        'informe_tecnico_nro_doc': requerimiento.informe_tecnico_nro or '__________',
        'comisaria_doc': vehiculo.subunidad.nombre if hasattr(vehiculo, 'subunidad') and vehiculo.subunidad else '[SUB UNIDAD NO ESPECIFICADA]',
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


# ¡REINTRODUCIDO!: API para buscar descripciones de servicio (para Select2)
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

# ¡REINTRODUCIDO!: API para crear una nueva descripción de servicio
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
    query = request.GET.get('q', '')
    if query:
        piezas = Pieza.objects.filter(nombre__icontains=query)[:10]
        results = [{'id': p.id, 'text': f"{p.nombre} (Stock: {p.stock_actual})"} for p in piezas]
    else:
        results = []
    return JsonResponse({'results': results})


def detalle_requerimiento_modal(request, id):
    requerimiento = get_object_or_404(Requerimiento.objects
                                 .select_related('vehiculo')
                                 .prefetch_related('detalles_servicio__detalle', # ¡CORREGIDO!: Accede via .detalle
                                                   'detalles_pieza__pieza'),
                                 id=id)
    
    context = {
        'requerimiento': requerimiento,
    }
    return render(request, 'requerimientos/detalle_requerimiento_modal.html', context)
