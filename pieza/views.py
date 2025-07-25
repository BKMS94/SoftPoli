from django.shortcuts import render, get_object_or_404, redirect
from .models import Pieza
from .forms import PiezaForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse, Http404

def pieza_lista(request):
    piezas = Pieza.objects.filter(
        nombre__icontains=request.GET.get('search', '')
    ).order_by('id')
    paginator = Paginator(piezas, 10)
    page_number = request.GET.get('page', 1)
    try:
        piezas = paginator.page(page_number)
    except EmptyPage:
        piezas = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        piezas = paginator.page(1)
    
    context = {
        'piezas': piezas,
        'urlindex': 'pieza_index',
        'urlcrear': 'pieza_crear'
    }
    return render(request, 'pieza/index.html', context)

def pieza_crear(request):
    if request.method == 'POST':
        form = PiezaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pieza creada correctamente.")
            return redirect('pieza_index')
    else:
        form = PiezaForm()
    context = {'form': form}
    return render(request, 'pieza/crear.html', context)

def pieza_detalle(request, id):
    pieza = get_object_or_404(Pieza, id=id)
    context = {'pieza': pieza}
    return render(request, 'pieza/detalle.html', context)

def pieza_editar(request, id):
    pieza = get_object_or_404(Pieza, id=id)
    if request.method == 'POST':
        form = PiezaForm(request.POST, instance=pieza)
        if form.is_valid():
            form.save()
            messages.success(request, "Pieza actualizada correctamente.")
            return redirect('pieza_index')
    else:
        form = PiezaForm(instance=pieza)
    context = {'form': form, 'pieza': pieza}
    return render(request, 'pieza/editar.html', context)

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