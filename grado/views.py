from django.shortcuts import render, get_object_or_404,redirect
from .models import Grado
from maestranza.utils import paginacion, modo_gestion
from django.contrib import messages
from .forms import GradosForm
from django.contrib.auth.decorators import login_required

# from django.http import Http404


# Create your views here.
@login_required
def grado_lista(request):
    grados = Grado.objects.filter(nombre__icontains= request.GET.get('search', '')).order_by('id')
    grados = paginacion(request, grados)
    content = {'grados': grados,
               'urlindex': 'grado_lista',
               'urlcrear': 'grado_crear'}
    return render(
        request, 'grado/lista.html', content
    )

@login_required
def grado_gestion(request, id=None):
    grado, modo, extra = modo_gestion(Grado,id)

    if request.method == 'POST':
        form = GradosForm(request.POST, instance=grado)
        if form.is_valid():
            try:
                grado = form.save()
                messages.success(request, f"Grado {'creado' if modo == 'crear' else 'actualizado'} correctamente.")
                return redirect('grado_lista')
            except Exception as e:
                messages.error(request, f"Error al guardar el Grado: {e}")
    else:
        form = GradosForm(instance=grado)
    context = {
        'form' : form,
        'grado': grado,
        'modo': modo,
        'extra': extra
    }
    return render(request, 'grado/gestion.html', context)


@login_required
def grado_detalle(request, id):
    grado = get_object_or_404(Grado, id=id)
    context = {'grado': grado}
    return render(request, 'grado/detalle.html',context)


@login_required  
def grado_borrar(request,id):
    grado = get_object_or_404(Grado, id=id)
    grado.delete()
    return redirect('grado_lista')