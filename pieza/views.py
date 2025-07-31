from django.shortcuts import render, get_object_or_404, redirect
from .models import Pieza
from .forms import PiezaForm
from django.contrib import messages
from maestranza.utils import modo_gestion, paginacion
from django.http import JsonResponse, Http404

def pieza_lista(request):
    piezas = Pieza.objects.filter(
        nombre__icontains=request.GET.get('search', '')
    ).order_by('id')
   
    piezas = paginacion(request, piezas)
    
    context = {
        'piezas': piezas,
        'urlindex': 'pieza_index',
        'urlcrear': 'pieza_crear'
    }
    return render(request, 'pieza/index.html', context)


def pieza_gestion(request, id=None):
    pieza, modo, extra = modo_gestion(Pieza,id)

    if request.method == 'POST':
        form =PiezaForm(request.POST, instance=pieza)
        if form.is_valid():
            try:
                pieza = form.save()
                messages.success(request, f"Pieza {'creada' if modo == 'crear' else 'actualizada'} correctamente.")
                return redirect('pieza_index')
            except Exception as e:
                messages.error(request, f"Error al guardar la pieza: {e}")
    else:
        form = PiezaForm(instance=pieza)
    context = {
        'form' : form,
        'pieza': pieza,
        'modo': modo,
        'extra': extra
    }
    return render(request, 'pieza/gestion.html', context)


def pieza_detalle(request, id):
    pieza = get_object_or_404(Pieza, id=id)
    context = {'pieza': pieza}
    return render(request, 'pieza/detalle.html', context)


def pieza_borrar(request, id):
    pieza = get_object_or_404(Pieza, id=id)
    pieza.delete()
    messages.success(request, "Pieza eliminada correctamente.")
    return redirect('pieza_index')

def pieza_stock(request, pieza_id):
    try:
        pieza = Pieza.objects.get(pk=pieza_id)
        return JsonResponse({'stock': pieza.cantidad_stock})
    except Pieza.DoesNotExist:
        raise Http404("Pieza no encontrada")