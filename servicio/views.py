from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from dal import autocomplete
from django.db.models import Q
from django.db import transaction
from .models import Servicio
from vehiculo.models import Vehiculo
from persona.models import Persona,Tecnico
from pieza.models import  Pieza
from .forms import ServicioForm, MovimientoStockFormSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Vistas para Servicio

def servicio_lista(request):
    search_query = request.GET.get('search', '')
    servicios = Servicio.objects.filter(Q(vehiculo__placa__icontains=search_query)) \
                               .order_by('-fecha')
    paginator = Paginator(servicios, 10)
    page_number = request.GET.get('page', 1)
    try:
        servicios = paginator.page(page_number)
    except EmptyPage:
        servicios = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        servicios = paginator.page(1)
    context = {'servicios': servicios,
               'urlindex': 'servicio_lista',
               'urlcrear': 'servicio_crear',
               'search_query': search_query}
    return render(request, 'servicio/index.html', context)

def servicio_form(request, id=None):
    if id:
        servicio = get_object_or_404(Servicio, id=id)
        modo = 'editar'
    else:
        servicio = None
        modo = 'crear'

    print(modo)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        formset = MovimientoStockFormSet(request.POST, instance=servicio)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    servicio = form.save()
                    # Actualiza el kilometraje del vehículo si corresponde
                    vehiculo = servicio.vehiculo
                    nuevo_kilometraje = servicio.kilometraje_act
                    if vehiculo.kilometraje < nuevo_kilometraje:
                        vehiculo.kilometraje = nuevo_kilometraje
                        vehiculo.save()
                    formset.instance = servicio
                    formset.save()
                return redirect('servicio_lista')
            except Exception as e:
                print("Error:", e)
    else:
        form = ServicioForm(instance=servicio)
        formset = MovimientoStockFormSet(instance=servicio)

    context = {
        'form': form,
        'formset': formset,
        'servicio': servicio,
        'modo': modo,
    }
    return render(request, 'servicio/crear.html', context)


# def servicio_editar(request, id):
#     servicio = get_object_or_404(Servicio, id=id)
#     if request.method == 'POST':
#         form = ServicioForm(request.POST, instance=servicio)
#         formset = MovimientoStockFormSet(request.POST, instance=servicio)
#         if form.is_valid() and formset.is_valid():
#             try:
#                 with transaction.atomic():
#                     servicio = form.save()
#                     # Actualiza el kilometraje del vehículo si corresponde
#                     vehiculo = servicio.vehiculo
#                     nuevo_kilometraje = servicio.kilometraje_act
#                     if vehiculo.kilometraje < nuevo_kilometraje:
#                         vehiculo.kilometraje = nuevo_kilometraje
#                         vehiculo.save()
#                     formset.instance = servicio
#                     formset.save()
#                 return redirect('servicio_lista')
#             except Exception as e:
#                 print("Error:", e)
#     else:
#         form = ServicioForm(instance=servicio)
#         formset = MovimientoStockFormSet(instance=servicio)
#     context = {'form': form, 'formset': formset, 'servicio': servicio, 'modo': 'crear',}
#     return render(request, 'servicio/editar.html', context)

def servicio_detalle(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    context = {'servicio': servicio}
    return render(request, 'servicio/detalle.html', context)

def servicio_borrar(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect('servicio_lista')


class VehiculoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Vehiculo.objects.all()
        if self.q:
            qs = qs.filter(placa__icontains=self.q)
        return qs
    
class PersonaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Persona.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs
    
class PiezaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Pieza.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs
    
class TecnicoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tecnico.objects.all()
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs