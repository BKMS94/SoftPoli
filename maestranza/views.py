from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from servicio.models import Servicio, Vehiculo, Persona, Tecnico, Pieza
from grado.models import  Grado
from ubicacion.models import  Unidad, SubUnidad
from tdr.models import Requerimiento
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'dashboard.html')

@login_required
def detalle_objeto_modal_html(request, tipo_objeto, pk):
    """
    Vista genérica que renderiza el HTML del modal para cualquier objeto.
    """
    try:
        template_name = None
        context = {}
        
        if tipo_objeto == 'servicio':
            objeto = get_object_or_404(Servicio.objects.prefetch_related('movimientostock_set__pieza'), pk=pk)
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
        elif tipo_objeto == 'pieza':
             objeto = get_object_or_404(Pieza, pk=pk)
             template_name = 'pieza/detalle.html'
             context = {'pieza': objeto}
        elif tipo_objeto == 'unidad':
             objeto = get_object_or_404(Unidad, pk=pk)
             template_name = 'unidad/detalle.html'
             context = {'unidad': objeto}
        elif tipo_objeto == 'subunidad':
             objeto = get_object_or_404(SubUnidad, pk=pk)
             template_name = 'subunidad/detalle.html'
             context = {'subunidad': objeto}
        elif tipo_objeto == 'tecnico':
             objeto = get_object_or_404(Tecnico, pk=pk)
             template_name = 'tecnico/detalle.html'
             context = {'tecnico': objeto}
        elif tipo_objeto == 'requerimiento':
             objeto = get_object_or_404(Requerimiento, pk=pk)
             template_name = 'requerimiento/detalle.html'
             context = {'requerimiento': objeto}
        
        if template_name and context:
            html_content = render_to_string(template_name, context, request)
            return HttpResponse(html_content)
        else:
            return HttpResponse('Tipo de objeto no soportado.', status=404)
    
    except Exception as e:
        return HttpResponse(f'Error al cargar los detalles: {e}', status=500)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # Cambia por tu vista principal
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'registration/login.html')