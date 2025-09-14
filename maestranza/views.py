from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from grado.models import Grado
from persona.models import Persona, Tecnico
from ubicacion.models import Unidad, SubUnidad
from tdr.models import Requerimiento
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from vehiculo.models import Vehiculo
from servicio.models import Servicio
from pieza.models import Pieza
from django.db.models import Count
from django.db import models
from datetime import timedelta


@login_required
def index(request):
    # Indicadores
    total_vehiculos = Vehiculo.objects.count()
    vehiculos_operativos = Vehiculo.objects.filter(estado_vehi="OPERATIVO").count()
    servicios_en_proceso = Servicio.objects.filter(estado="EN PROCESO").count()
    tdrs_generados = Requerimiento.objects.count()
    piezas_bajo_stock_list = Pieza.objects.filter(
        cantidad_stock__lte=models.F("reorder")
    ).order_by("cantidad_stock", "nombre")
    piezas_bajo_stock = piezas_bajo_stock_list.count()
    total_servicios = Servicio.objects.count()
    servicios_finalizados = Servicio.objects.filter(estado="FINALIZADO").count()
    porcentaje_cumplimiento = (
        round(servicios_finalizados / total_servicios * 100, 1)
        if total_servicios > 0
        else 0
    )

    # Vehículos por estado para gráfico de pastel
    vehiculos_estado = Vehiculo.objects.values("estado_vehi").annotate(
        total=Count("id")
    )
    vehiculos_labels = []
    vehiculos_data = []
    for estado in ["OPERATIVO", "INOPERATIVO", "MANTENIMIENTO"]:
        vehiculos_labels.append(estado.replace("_", " ").capitalize())
        total = next(
            (
                item["total"]
                for item in vehiculos_estado
                if item["estado_vehi"] == estado
            ),
            0,
        )
        vehiculos_data.append(total)

    # Servicios finalizados por mes (últimos 12 meses)
    hoy = timezone.now().date()
    servicios_por_mes_labels = []
    servicios_por_mes_data = []
    for i in range(11, -1, -1):
        mes = hoy.replace(day=1) - timedelta(days=30 * i)
        servicios_por_mes_labels.append(mes.strftime("%b %Y"))
        count = Servicio.objects.filter(
            estado="FINALIZADO", fecha_fin__year=mes.year, fecha_fin__month=mes.month
        ).count()
        servicios_por_mes_data.append(count)

    context = {
        "total_vehiculos": total_vehiculos,
        "vehiculos_operativos": vehiculos_operativos,
        "servicios_en_proceso": servicios_en_proceso,
        "tdrs_generados": tdrs_generados,
        "piezas_bajo_stock": piezas_bajo_stock,
        "piezas_bajo_stock_list": piezas_bajo_stock_list,
        "vehiculos_labels": vehiculos_labels,
        "vehiculos_data": vehiculos_data,
        "servicios_por_mes_labels": servicios_por_mes_labels,
        "servicios_por_mes_data": servicios_por_mes_data,
        "total_servicios": total_servicios,
        "servicios_finalizados": servicios_finalizados,
        "porcentaje_cumplimiento": porcentaje_cumplimiento,
    }
    return render(request, "dashboard.html", context)


@login_required
def detalle_objeto_modal_html(request, tipo_objeto, pk):
    """
    Vista genérica que renderiza el HTML del modal para cualquier objeto.
    """
    try:
        template_name = None
        context = {}

        if tipo_objeto == "servicio":
            objeto = get_object_or_404(
                Servicio.objects.prefetch_related("movimientostock_set__pieza"), pk=pk
            )
            template_name = "servicio/detalle.html"
            context = {"servicio": objeto}
        elif tipo_objeto == "vehiculo":
            objeto = get_object_or_404(Vehiculo, pk=pk)
            template_name = "vehiculo/detalle.html"
            context = {"vehiculo": objeto}
        elif tipo_objeto == "persona":
            objeto = get_object_or_404(Persona, pk=pk)
            template_name = "persona/detalle.html"
            context = {"persona": objeto}
        elif tipo_objeto == "grado":
            objeto = get_object_or_404(Grado, pk=pk)
            template_name = "grado/detalle.html"
            context = {"grado": objeto}
        elif tipo_objeto == "pieza":
            objeto = get_object_or_404(Pieza, pk=pk)
            template_name = "pieza/detalle.html"
            context = {"pieza": objeto}
        elif tipo_objeto == "unidad":
            objeto = get_object_or_404(Unidad, pk=pk)
            template_name = "unidad/detalle.html"
            context = {"unidad": objeto}
        elif tipo_objeto == "subunidad":
            objeto = get_object_or_404(SubUnidad, pk=pk)
            template_name = "subunidad/detalle.html"
            context = {"subunidad": objeto}
        elif tipo_objeto == "tecnico":
            objeto = get_object_or_404(Tecnico, pk=pk)
            template_name = "tecnico/detalle.html"
            context = {"tecnico": objeto}
        elif tipo_objeto == "requerimiento":
            objeto = get_object_or_404(Requerimiento, pk=pk)
            template_name = "requerimiento/detalle.html"
            context = {"requerimiento": objeto}

        if template_name and context:
            html_content = render_to_string(template_name, context, request)
            return HttpResponse(html_content)
        else:
            return HttpResponse("Tipo de objeto no soportado.", status=404)

    except Exception as e:
        return HttpResponse(f"Error al cargar los detalles: {e}", status=500)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")  # Cambia por tu vista principal
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "registration/login.html")
