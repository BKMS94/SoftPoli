from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from servicio.models import Servicio, Vehiculo, Persona
from grado.models import  Grado
from ubicacion.models import  Unidad, SubUnidad

def index(request):
    return render(request, 'dashboard.html')


def detalle_objeto_modal_html(request, tipo_objeto, pk):
    """
    Vista genérica que renderiza el HTML del modal para cualquier objeto.
    """
    try:
        template_name = None
        context = {}
        
        if tipo_objeto == 'servicio':
            objeto = get_object_or_404(Servicio, pk=pk)
            template_name = 'servicio/detalle.html'
            context = {'servicio': objeto}
        elif tipo_objeto == 'vehiculo':
            objeto = get_object_or_404(Vehiculo, pk=pk)
            template_name = 'vehiculo/detalle.html'
            context = {'vehiculo': objeto}
        elif tipo_objeto == 'persona':
             objeto = get_object_or_404(Persona, pk=pk)
             template_name = 'persona/detalle.html'
             context = {'persona': objeto}
        elif tipo_objeto == 'grado':
             objeto = get_object_or_404(Grado, pk=pk)
             template_name = 'grado/detalle.html'
             context = {'grado': objeto}
        elif tipo_objeto == 'unidad':
             objeto = get_object_or_404(Unidad, pk=pk)
             template_name = 'unidad/detalle.html'
             context = {'unidad': objeto}
        
        if template_name and context:
            html_content = render_to_string(template_name, context, request)
            return HttpResponse(html_content)
        else:
            return HttpResponse('Tipo de objeto no soportado.', status=404)
    
    except Exception as e:
        return HttpResponse(f'Error al cargar los detalles: {e}', status=500)