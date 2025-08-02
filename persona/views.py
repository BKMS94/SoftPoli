from maestranza.utils import paginacion, modo_gestion
from django.shortcuts import render, get_object_or_404,redirect
from .models import Persona, Tecnico
from .forms import PersonaForm, TecnicoForm, TelefonoCleanMixin as forms
from django.contrib import messages

# Create your views here.

def persona_index(request):
    personas = Persona.objects.filter(codigo__contains= request.GET.get('search', '')).order_by('id')
    personas = paginacion(request, personas)
    context = {'personas': personas,
               'urlindex': 'persona_index',
               'urlcrear': 'persona_crear'}
    return render(request, 'persona/index.html', context)


def persona_gestion(request, id=None):
    persona, modo,extra = modo_gestion(Persona,id)

    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            try:
                persona = form.save()
                messages.success(request, f'Persona{'creado' if modo == 'crear' else 'actualizado'} correctamente.')
                return redirect('persona_index')
            except Exception as e:
                messages.error( request, f'Error al guardar la persona: {e}')
    else:
        form = PersonaForm(instance=persona)    
    context = {
        'form' : form,
        'persona' : persona,
        'modo' : modo
    }
    return render(request, 'persona/gestion.html', context)



def persona_detalle(request,id):
    persona = get_object_or_404(Persona, id=id)
    context = {'persona':persona}
    return render(request, 'persona/detalle.html', context)



def persona_borrar(request,id):
    persona = get_object_or_404(Persona, id=id)
    persona.delete()
    return redirect('persona_index')


def tecnico_index(request):
    tecnicos = Tecnico.objects.filter(nombre__contains= request.GET.get('search', ''))
    tecnicos = paginacion(request, tecnicos)
    context = {'tecnicos': tecnicos,
               'urlindex': 'tecnico_index',
               'urlcrear': 'tecnico_crear'}
    return render(request, 'tecnico/index.html', context)


def tecnico_gestion(request, id=None):
    tecnico, modo,extra = modo_gestion(Tecnico,id)

    if request.method == 'POST':
        form = TecnicoForm(request.POST, instance=tecnico)
        if form.is_valid():
            try:
                tecnico = form.save()
                messages.success(request, f'Técnico{'creado' if modo == 'crear' else 'actualizado'} correctamente.')
                return redirect('tecnico_index')
            except Exception as e:
                messages.error( request, f'Error al guardar el técnico: {e}')
    else:
        form = TecnicoForm(instance=tecnico)    
    context = {
        'form' : form,
        'tecnico' : tecnico,
        'modo' : modo
    }
    return render(request, 'tecnico/gestion.html', context)


def tecnico_detalle(request,id):
    tecnico = get_object_or_404(Tecnico, id=id)
    context = {'tecnico':tecnico}
    return render(request, 'tecnico/detalle.html', context)

def tecnico_borrar(request,id):
    tecnico = get_object_or_404(Tecnico, id=id)
    tecnico.delete()
    return redirect('tecnico_index')

def clean_telefono(self):
    telefono = self.cleaned_data['telefono']
    if not telefono.isdigit():
        raise forms.ValidationError("El teléfono debe contener solo números.")
    if len(telefono) < 7 or len(telefono) > 12:
        raise forms.ValidationError("El teléfono debe tener entre 7 y 12 dígitos.")
    return telefono