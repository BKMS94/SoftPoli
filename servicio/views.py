from django.shortcuts import render, get_object_or_404, redirect
from .models import Servicio, MovimientoStock
from .forms import ServicioForm, MovimientoStockForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Vistas para Servicio

def servicio_lista(request):
    servicios = Servicio.objects.all()
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page', 1)
    try:
        servicios = paginator.page(page_number)
    except PageNotAnInteger:
        servicios = paginator.page(1)
    except EmptyPage:
        servicios = paginator.page(paginator.num_pages)
    context = {'servicios': servicios}
    return render(request, 'servicio/index.html', context)

def servicio_crear(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            vehiculo = servicio.vehiculo
            vehiculo.kilometraje = servicio.kilometraje_act
            vehiculo.save()
            servicio.save()
            return redirect('servicio_lista')
    else:
        form = ServicioForm()
    context = {'form': form}
    return render(request, 'servicio/crear.html', context)

def servicio_detalle(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    context = {'servicio': servicio}
    return render(request, 'servicio/detalle.html', context)

def servicio_editar(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('servicio_lista')
    else:
        form = ServicioForm(instance=servicio)
    context = {'form': form, 'servicio': servicio}
    return render(request, 'servicio/editar.html', context)

def servicio_borrar(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect('servicio_lista')

# Vistas para MovimientoStock

def movimiento_lista(request):
    movimientos = MovimientoStock.objects.all()
    paginator = Paginator(movimientos, 10)
    page_number = request.GET.get('page', 1)
    try:
        movimientos = paginator.page(page_number)
    except PageNotAnInteger:
        movimientos = paginator.page(1)
    except EmptyPage:
        movimientos = paginator.page(paginator.num_pages)
    context = {'movimientos': movimientos}
    return render(request, 'movimiento/index.html', context)

def movimiento_crear(request):
    if request.method == 'POST':
        form = MovimientoStockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movimiento_lista')
    else:
        form = MovimientoStockForm()
    context = {'form': form}
    return render(request, 'movimiento/crear.html', context)

def movimiento_detalle(request, id):
    movimiento = get_object_or_404(MovimientoStock, id=id)
    context = {'movimiento': movimiento}
    return render(request, 'movimiento/detalle.html', context)

def movimiento_editar(request, id):
    movimiento = get_object_or_404(MovimientoStock, id=id)
    if request.method == 'POST':
        form = MovimientoStockForm(request.POST, instance=movimiento)
        if form.is_valid():
            form.save()
            return redirect('movimiento_lista')
    else:
        form = MovimientoStockForm(instance=movimiento)
    context = {'form': form, 'movimiento': movimiento}
    return render(request, 'movimiento/editar.html', context)

def movimiento_borrar(request, id):
    movimiento = get_object_or_404(MovimientoStock, id=id)
    movimiento.delete()
    return redirect('movimiento_lista')