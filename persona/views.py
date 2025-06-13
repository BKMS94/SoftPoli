from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import render, get_object_or_404,redirect
from .models import Persona, Tecnico
from .forms import PersonaForm, TecnicoForm

# Create your views here.

def persona_index(request):
    personas = Persona.objects.filter(codigo__contains= request.GET.get('search', ''))
    paginator = Paginator(personas, 10)
    page_number = request.GET.get('page',1)
    try:
        personas = paginator.page(page_number)
    except EmptyPage:
        personas = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        personas = paginator.page(1)
    context = {'personas': personas,
               'urlindex': 'persona_index',
               'urlcrear': 'persona_crear'}
    return render(request, 'persona/index.html', context)

def persona_crear(request):
    if request.method =='POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('persona_index')
    else:
        form= PersonaForm()
        context= {'form':form}
        return render(request, 'persona/crear.html', context)


def persona_detalle(request,id):
    persona = get_object_or_404(Persona, id=id)
    context = {'persona':persona}
    return render(request, 'persona/detalle.html', context)

def persona_editar(request,id):
    persona = get_object_or_404(Persona, id=id)
    if  request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('persona_index')
    else:
        form = PersonaForm(instance=persona)
        context = {'persona': persona, 'form':form}
        return render(request, 'persona/editar.html', context)

def persona_borrar(request,id):
    persona = get_object_or_404(Persona, id=id)
    persona.delete()
    return redirect('persona_index')


def tecnico_index(request):
    tecnicos = Tecnico.objects.filter(codigo__contains= request.GET.get('search', ''))
    paginator = Paginator(tecnicos, 10)
    page_number = request.GET.get('page',1)
    try:
        tecnicos = paginator.page(page_number)
    except EmptyPage:
        tecnicos = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        tecnicos = paginator.page(1)
    context = {'tecnicos': tecnicos,
               'urlindex': 'tecnico_index',
               'urlcrear': 'tecnico_crear'}
    return render(request, 'tecnico/index.html', context)

def tecnico_crear(request):
    if request.method =='POST':
        form = TecnicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tecnico_index')
    else:
        form= TecnicoForm()
        context= {'form':form}
        return render(request, 'tecnico/crear.html', context)


def tecnico_detalle(request,id):
    tecnico = get_object_or_404(Tecnico, id=id)
    context = {'tecnico':tecnico}
    return render(request, 'tecnico/detalle.html', context)

def tecnico_editar(request,id):
    tecnico = get_object_or_404(Tecnico, id=id)
    if  request.method == 'POST':
        form = TecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            form.save()
            return redirect('tecnico_index')
    else:
        form = TecnicoForm(instance=tecnico)
        context = {'tecnico': tecnico, 'form':form}
        return render(request, 'tecnico/editar.html', context)

def tecnico_borrar(request,id):
    tecnico = get_object_or_404(Tecnico, id=id)
    tecnico.delete()
    return redirect('tecnico_index')