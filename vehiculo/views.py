from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.http import JsonResponse
from maestranza.utils import paginacion,modo_gestion
from .models import Vehiculo
from .forms import VehiculoForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def vehiculo_lista(request):
    vehiculos = Vehiculo.objects.filter(placa_int__icontains= request.GET.get('search', '')).order_by('id') 
    vehiculos = paginacion(request,vehiculos)
    context = {'vehiculos': vehiculos,
               'urlindex': 'vehiculo_index',
               'urlcrear': 'vehiculo_crear'}
    return render(request, 'vehiculo/index.html', context)


@login_required
def vehiculo_gestion(request, id=None):
    vehiculos, modo, extra = modo_gestion(Vehiculo,id)

    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculos)
        if form.is_valid():
            try:
                vehiculos = form.save()
                messages.success(request, f"Vehículo {'creado' if modo == 'crear' else 'actualizado'} correctamente.")
                return redirect('vehiculo_index')
            except Exception as e:
                messages.error(request, f"Error al guardar el vehículos: {e}")
    else:
        form = VehiculoForm(instance=vehiculos)
    context = {
        'form' : form,
        'vehiculos': vehiculos,
        'modo': modo,
        'extra': extra
    }
    return render(request, 'vehiculo/gestion.html', context)


@login_required
def vehiculo_detalle(request,id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    context = {'vehiculo':vehiculo}
    return render(request, 'vehiculo/detalle.html', context)


@login_required
def vehiculo_borrar(request,id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    return redirect('vehiculo_index')

# @login_required
def vehiculo_kilometraje(request, id):
    try:
        vehiculo = get_object_or_404(Vehiculo, id=id)
        kilometraje = vehiculo.kilometraje  # Ajusta el nombre del campo si es diferente
    except Vehiculo.DoesNotExist:
        kilometraje = 0
    return JsonResponse({'kilometraje': kilometraje})