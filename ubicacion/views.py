from django.shortcuts import render, get_object_or_404, redirect
from .models import SubUnidad, Unidad
from maestranza.utils import paginacion, modo_gestion
from django.contrib import messages
from .forms import UnidadForm, SubunidadForm
from dal import autocomplete
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def unidad_lista(request):
    unidades = Unidad.objects.filter(
        nombre__icontains= request.GET.get('search', '')). order_by('id')
    unidades = paginacion(request, unidades)
    context = {
        'unidades': unidades,
        'urlindex' : 'unidad_index',
        'urlcrear' : 'unidad_crear',
    }
    return render(request, 'unidad/index.html', context)

@login_required
def unidad_gestion(request, id=None):
    unidades, modo, extra = modo_gestion(Unidad,id)

    if request.method == 'POST':
        form = UnidadForm(request.POST, instance=unidades)
        if form.is_valid():
            try:
                unidades = form.save()
                messages.success(request, f"Unidad {'creada' if modo == 'crear' else 'actualizada'} correctamente.")
                return redirect('unidad_index')
            except Exception as e:
                messages.error(request, f"Error al guardar la Unidad: {e}")
    else:
        form = UnidadForm(instance=unidades)
    context = {
        'form' : form,
        'unidades': unidades,
        'modo': modo,
        'extra': extra
    }
    return render(request, 'unidad/gestion.html', context)
    
@login_required
def unidad_detalle(request, id):
    unidad = get_object_or_404(Unidad, id=id)
    context = {'unidad': unidad}
    return render(request, 'unidad/detalle.html', context)

@login_required
def unidad_borrar(request, id):
    unidad = get_object_or_404(Unidad, id=id)
    unidad.delete()
    return redirect('unidad_index')

@login_required
def subunidad_lista(request):
    subunidades = SubUnidad.objects.filter(
        nombre__icontains= request.GET.get('search', '')). order_by('id')
    subunidades = paginacion(request, subunidades)
    context = {
        'subunidades': subunidades,
        'urlindex' : 'subunidad_index',
        'urlcrear' : 'subunidad_crear',
    }
    return render(request, 'subunidad/index.html', context)

@login_required
def subunidad_gestion(request, id=None):
    subunidades, modo, extra = modo_gestion(SubUnidad,id)

    if request.method == 'POST':
        form = SubunidadForm(request.POST, instance=subunidades)
        if form.is_valid():
            try:
                subunidades = form.save()
                messages.success(request, f"Sub unidad {'creada' if modo == 'crear' else 'actualizada'} correctamente.")
                return redirect('subunidad_index')
            except Exception as e:
                messages.error(request, f"Error al guardar la Sub unidad: {e}")
    else:
        form = SubunidadForm(instance=subunidades)
    context = {
        'form' : form,
        'subunidades': subunidades,
        'modo': modo,
        'extra': extra
    }
    return render(request, 'subunidad/gestion.html', context)

@login_required  
def subunidad_detalle(request, id):
    subunidad = get_object_or_404(SubUnidad, id=id)
    context = {'subunidad': subunidad}
    return render(request, 'subunidad/detalle.html', context)

@login_required
def subunidad_borrar(request, id):
    subunidad = get_object_or_404(SubUnidad, id=id)
    subunidad.delete()
    return redirect('subunidad_index')


class UnidadAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Unidad.objects.all().order_by('id')
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs
    

class SubUnidadAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SubUnidad.objects.all().order_by('id')
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs