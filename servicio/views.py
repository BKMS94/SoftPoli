from django.shortcuts import render, get_object_or_404, redirect
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
    servicios = Servicio.objects.filter(Q(vehiculo__placa__icontains=search_query))
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

def servicio_crear(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        formset = MovimientoStockFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el servicio principal
                    servicio = form.save()
                    # Asignar el servicio a cada movimiento y guardar el formset
                    formset.instance = servicio
                    formset.save()
                return redirect('servicio_lista')
            except Exception as e:
                # Si algo falla, nada se guarda
                print("Error:", e)
    else:
        form = ServicioForm()
        formset = MovimientoStockFormSet()
    context = {'form': form, 'formset': formset,
               'urlindex': 'servicio_lista',
               'urlcrear': 'servicio_crear'} 
    return render(request, 'servicio/crear.html', context)


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