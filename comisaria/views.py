from django.shortcuts import render, get_object_or_404, redirect
from .models import Comisaria
from maestranza.utils import paginacion, modo_gestion
from django.contrib import messages
from .forms import ComisariaForm

# Create your views here.

def comisaria_lista(request):
    comisarias = Comisaria.objects.filter(
        nombre__icontains= request.GET.get('search', '')). order_by('id')
    comisarias = paginacion(request, comisarias)
    context = {
        'comisarias': comisarias,
        'urlindex' : 'comisaria_index',
        'urlcrear' : 'comisaria_crear',
    }
    return render(request, 'comisaria/index.html', context)


def comisaria_gestion(request, id=None):
    comisaria, modo, extra = modo_gestion(Comisaria,id)

    if request.method == 'POST':
        form = ComisariaForm(request.POST, instance=comisaria)
        if form.is_valid():
            try:
                comisaria = form.save()
                messages.success(request, f"Comisaría {'creado' if modo == 'crear' else 'actualizado'} correctamente.")
                return redirect('comisaria_index')
            except Exception as e:
                messages.error(request, f"Error al guardar la Comisaría: {e}")
    else:
        form = ComisariaForm(instance=comisaria)
    context = {
        'form' : form,
        'comisaria': comisaria,
        'modo': modo,
        'extra': extra
    }
    return render(request, 'comisaria/gestion.html', context)
    
def comisaria_detalle(request, id):
    pass

def comisaria_borrar(request, id):
    pass


