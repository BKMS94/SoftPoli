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
from django.utils import timezone
from vehiculo.models import Vehiculo
from servicio.models import Servicio
from pieza.models import Pieza
from tdr.models import Requerimiento
from django.db.models import Count
from datetime import timedelta

@login_required
def index(request):
   # Indicadores
    total_vehiculos = Vehiculo.objects.count()
    vehiculos_en_servicio = Vehiculo.objects.filter(estado_vehi='OPERATIVO').count()
    servicios_en_proceso = Servicio.objects.filter(estado='EN PROCESO').count()
    mantenimientos_pendientes = Servicio.objects.filter(estado='PENDIENTE').count()
    piezas_bajo_stock = Pieza.objects.filter(cantidad_stock__lte=5).count()

    # Servicios por estado para gráfico de barras
    servicios_estado = Servicio.objects.values('estado').annotate(total=Count('id'))
    servicios_labels = []
    servicios_data = []
    for estado in ['EN PROCESO', 'FINALIZADO']:
        servicios_labels.append(estado.capitalize())
        total = next((item['total'] for item in servicios_estado if item['estado'] == estado), 0)
        servicios_data.append(total)

    # Vehículos por estado para gráfico de pastel
    vehiculos_estado = Vehiculo.objects.values('estado_vehi').annotate(total=Count('id'))
    vehiculos_labels = []
    vehiculos_data = []
    for estado in ['OPERATIVO', 'INOPERATIVO', 'MANTENIMIENTO']:
        vehiculos_labels.append(estado.replace('_', ' ').capitalize())
        total = next((item['total'] for item in vehiculos_estado if item['estado_vehi'] == estado), 0)
        vehiculos_data.append(total)

    # TDRs generados por mes (últimos 12 meses)
    hoy = timezone.now().date()
    meses = []
    tdrs_por_mes = []
    for i in range(11, -1, -1):
        mes = (hoy.replace(day=1) - timedelta(days=30*i))
        meses.append(mes.strftime('%b %Y'))
        tdrs_count = Requerimiento.objects.filter(
            fecha_creacion__year=mes.year,
            fecha_creacion__month=mes.month
        ).count()
        tdrs_por_mes.append(tdrs_count)

    context = {
        'total_vehiculos': total_vehiculos,
        'vehiculos_en_servicio': vehiculos_en_servicio,
        'servicios_en_proceso': servicios_en_proceso,
        'mantenimientos_pendientes': mantenimientos_pendientes,
        'piezas_bajo_stock': piezas_bajo_stock,
        'servicios_labels': servicios_labels,
        'servicios_data': servicios_data,
        'vehiculos_labels': vehiculos_labels,
        'vehiculos_data': vehiculos_data,
        'meses': meses,
        'tdrs_por_mes': tdrs_por_mes,
    }
    return render(request, 'dashboard.html', context)


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
