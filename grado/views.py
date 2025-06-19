from django.shortcuts import render, get_object_or_404,redirect
from .models import Grado
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import GradosForm

# from django.http import Http404


# Create your views here.

def grado_lista(request):
    grados_list = Grado.objects.filter(nombre__icontains= request.GET.get('search', '')).order_by('id')
    paginator = Paginator(grados_list, 10)
    page_numbre = request.GET.get('page',1)
    try:
        grados = paginator.page(page_numbre)
    except EmptyPage:
        grados = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        grados = paginator.page(1)
    content = {'grados': grados,
               'urlindex': 'grado_lista',
               'urlcrear': 'grado_crear'}
    return render(
        request, 'grado/lista.html', content
    )


def grado_crear(request):
    if request.method == 'POST':
        form = GradosForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('grado_lista')

    else:
        form = GradosForm()
        context = {'form':form}
        return render(request,'grado/crear.html',context)
        

def grado_detalle(request, id):
    grado = get_object_or_404(Grado, id=id)
    context = {'grado': grado}
    return render(request, 'grado/detalle.html',context)


def grado_editar(request,id):
    grado = get_object_or_404(Grado, id=id)
    if request.method == 'POST':
        form = GradosForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()
            return redirect('grado_lista')
    else:
        form = GradosForm(instance=grado)
        context = {'form':form, 'grado':grado}
        return render(request,'grado/editar.html', context)
    
def grado_borrar(request,id):
    grado = get_object_or_404(Grado, id=id)
    grado.delete()
    return redirect('grado_lista')