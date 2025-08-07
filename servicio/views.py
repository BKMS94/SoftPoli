from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Servicio, MovimientoStock,Persona,Pieza,Vehiculo,Tecnico
from .forms import ServicioForm, MovimientoStockForm
from maestranza.utils import paginacion, modo_gestion
from django.forms import inlineformset_factory
from django.db.models import Q
from dal import autocomplete
# from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.utils import timezone

# Vistas para Servicio

# @login_required
def servicio_lista(request):
    search_query = request.GET.get('search', '')
    servicios = Servicio.objects.filter(
        Q(vehiculo__placa_int__icontains=search_query) |
        Q(persona__nombre__icontains=search_query) |
        Q(tecnico__nombre__icontains=search_query)
    ).order_by('-fecha')
    
    servicios = paginacion(request, servicios)
    
    context = {
        'servicios': servicios,
        'urlindex': 'servicio_lista',
        'urlcrear': 'servicio_crear',
        'search_query': search_query
    }
    return render(request, 'servicio/index.html', context)

# @login_required
def servicio_form(request, id=None):
   
    servicio, modo, extra = modo_gestion(Servicio,id)

    MovimientoStockFormSet = inlineformset_factory(
        Servicio,
        MovimientoStock,
        form=MovimientoStockForm,
        extra=extra,
        can_delete=True,
        fields=['pieza', 'cantidad']
    )

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        formset = MovimientoStockFormSet(request.POST, instance=servicio)
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    servicio = form.save()
                    vehiculo = servicio.vehiculo
                    nuevo_kilometraje = servicio.kilometraje_act
                    if vehiculo.kilometraje < nuevo_kilometraje:
                        vehiculo.kilometraje = nuevo_kilometraje
                        vehiculo.save()

                    formset.instance = servicio

                    movimientos_antes = {m.pk: m for m in MovimientoStock.objects.filter(servicio=servicio)} if servicio.pk else {}

                    # Procesa eliminaciones
                    for f in formset.deleted_forms:
                        movimiento = f.instance
                        if movimiento.pk and movimiento.pieza:
                            pieza = movimiento.pieza
                            pieza.cantidad_stock += movimiento.cantidad
                            pieza.save()
                        movimiento.delete()

                    # Procesa creaciones y actualizaciones
                    for f in formset.forms:
                        if not f.cleaned_data or f.cleaned_data.get('DELETE'):
                            continue
                        movimiento = f.save(commit=False)
                        pieza = movimiento.pieza
                        cantidad_nueva = movimiento.cantidad

                        if movimiento.pk in movimientos_antes:
                            cantidad_anterior = movimientos_antes[movimiento.pk].cantidad
                            pieza.cantidad_stock += cantidad_anterior
                        else:
                            cantidad_anterior = 0

                        if pieza.cantidad_stock - cantidad_nueva < 0:
                            raise Exception(f"No hay suficiente stock para la pieza {pieza.nombre}")
                        pieza.cantidad_stock -= cantidad_nueva
                        pieza.save()
                        movimiento.servicio = servicio
                        movimiento.save()

                    formset.save()

                messages.success(request, f"Servicio {'creado' if modo == 'crear' else 'actualizado'} correctamente.")
                return redirect('servicio_lista')
            except Exception as e:
                messages.error(request, f"Error al guardar el servicio: {e}")
        # Si hay error de validación, sigue mostrando el form con los datos ingresados
    else:
        form = ServicioForm(instance=servicio)
        formset = MovimientoStockFormSet(instance=servicio)

    context = {
        'form': form,
        'formset': formset,
        'servicio': servicio,
        'modo': modo
    }
    return render(request, 'servicio/gestion.html', context)

# @login_required
def servicio_detalle(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    context = {'servicio': servicio}
    return render(request, 'servicio/detalle.html', context)

# @login_required
def servicio_borrar(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect('servicio_lista')


class VehiculoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Vehiculo.objects.all().order_by('id')
        if self.q:
            qs = qs.filter(placa__icontains=self.q)
        return qs
    
class PersonaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Persona.objects.all().order_by('id')
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs
    
class PiezaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Pieza.objects.all().order_by('id')
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs
    
class TecnicoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tecnico.objects.all().order_by('id')
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)
        return qs

def generar_pdf_servicio(request, id):
    servicio = get_object_or_404(Servicio.objects.prefetch_related('movimientostock_set__pieza'), pk=id)
    vehiculo = servicio.vehiculo
    movimientos_stock = servicio.movimientostock_set.all() 
    
    html_string = render_to_string(
        'pdf/pdf_servicios.html',
        {
            'servicio': servicio,
            'vehiculo': vehiculo,
            'movimientos_stock': movimientos_stock,
            'logo_url': request.build_absolute_uri('/static/img/sello-pnp.png'),
            'fecha_actual': timezone.now(),
        }
    )
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="servicio_{servicio.id}.pdf"'
    return response