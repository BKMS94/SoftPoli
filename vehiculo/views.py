
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http import JsonResponse
from maestranza.utils import paginacion
from .models import Vehiculo
from .forms import VehiculoForm

# Create your views here.

def vehiculo_lista(request):
    vehiculos = Vehiculo.objects.filter(placa__icontains= request.GET.get('search', '')).order_by('id') 
    vehiculos = paginacion(request,vehiculos)
    context = {'vehiculos': vehiculos,
               'urlindex': 'vehiculo_index',
               'urlcrear': 'vehiculo_crear'}
    return render(request, 'vehiculo/index.html', context)

def vehiculo_crear(request):
    if request.method =='POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehiculo_index')
    else:
        form= VehiculoForm()
        context= {'form':form}
        return render(request, 'vehiculo/crear.html', context)


def vehiculo_detalle(request,id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    context = {'vehiculo':vehiculo}
    return render(request, 'vehiculo/detalle.html', context)

def vehiculo_editar(request,id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    if  request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('vehiculo_index')
    else:
        form = VehiculoForm(instance=vehiculo)
        context = {'vehiculo': vehiculo, 'form':form}
        return render(request, 'vehiculo/editar.html', context)

def vehiculo_borrar(request,id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    return redirect('vehiculo_index')

def vehiculo_kilometraje(request, pk):
    try:
        vehiculo = Vehiculo.objects.get(pk=pk)
        kilometraje = vehiculo.kilometraje  # Ajusta el nombre del campo si es diferente
    except Vehiculo.DoesNotExist:
        kilometraje = 0
    return JsonResponse({'kilometraje': kilometraje})