import os
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from fpdf import FPDF

# Importa los modelos necesarios
from maestranza.utils import modo_gestion, paginacion
from .models import Requerimiento, RequerimientoDescripcionDetalle, RequerimientoPiezaDetalle, DescripcionServicio # ¡Reintroducido DescripcionServicio!
from .forms import RequerimientoForm, RequerimientoPiezaDetalleForm, RequerimientoDescripcionDetalleForm
from pieza.models import PiezaTDR # Necesario para buscar_piezas_api
from .models import ConsolidadoTDR
from django.contrib.auth.decorators import login_required

# --- Vistas CRUD para Requerimientos (Funciones) ---
@login_required
def requerimiento_lista(request):
    search_query = request.GET.get('search', '')
    requerimientos = Requerimiento.objects.filter(
        Q(vehiculo__placa_int__icontains=search_query)
    ).order_by('-fecha_creacion')
    
    requerimientos = paginacion(request, requerimientos) 
    
    context = {
        'requerimientos': requerimientos,
        'urlindex': 'lista_requerimientos', 
        'urlcrear': 'crear_requerimiento', 
        'search_query': search_query
    }
    return render(request, 'requerimiento/index.html', context)

@login_required
def detalle_requerimiento(request, id):
    requerimiento =get_object_or_404(Requerimiento, id=id)
    context = {
        'requerimiento': requerimiento
    }
    return render(request, 'requerimiento/detalle.html', context)

@login_required
def requerimiento_form(request, id=None):
    requerimiento, modo, extra = modo_gestion(Requerimiento, id)

    RequerimientoDescripcionDetalleFormSet = inlineformset_factory(
        Requerimiento,
        RequerimientoDescripcionDetalle,
        form=RequerimientoDescripcionDetalleForm,
        extra=extra,
        can_delete=True,
        fields=['detalle_servicio'] # ¡CORREGIDO!: Ahora usa el ForeignKey 'detalle'
    )

    RequerimientoPiezaDetalleFormSet = inlineformset_factory(
        Requerimiento,
        RequerimientoPiezaDetalle,
        form=RequerimientoPiezaDetalleForm,
        extra=extra,
        can_delete=True,
        fields=['detalle_pieza', 'cantidad'],
    )

    if request.method == 'POST':
        form = RequerimientoForm(request.POST, instance=requerimiento)
        servicio_detalle_formset = RequerimientoDescripcionDetalleFormSet(request.POST, instance=requerimiento, prefix='serviciodetalle') # <<<< ASEGURA QUE ES 'serviciodetalle'
        pieza_detalle_formset = RequerimientoPiezaDetalleFormSet(request.POST, instance=requerimiento, prefix='piezadetalle') # <<<< ASEGURA QUE ES 'piezadetalle'
        
        if form.is_valid() and servicio_detalle_formset.is_valid() and pieza_detalle_formset.is_valid():
            with transaction.atomic():
                requerimiento = form.save() 

                servicio_detalle_formset.instance = requerimiento
                servicio_detalle_formset.save()

                pieza_detalle_formset.instance = requerimiento
                pieza_detalle_formset.save()
            
            messages.success(request, f'Requerimiento (TDR) {"creado" if modo == "crear" else "actualizado"} exitosamente.')
            return redirect('lista_requerimientos') 
        else:
            messages.error(request, f'Error al {"crear" if modo == "crear" else "actualizar"} el requerimiento. Revise los campos.')
    else: 
        form = RequerimientoForm(instance=requerimiento)
        servicio_detalle_formset = RequerimientoDescripcionDetalleFormSet(instance=requerimiento, prefix='serviciodetalle') # <<<< ASEGURA QUE ES 'serviciodetalle'
        pieza_detalle_formset = RequerimientoPiezaDetalleFormSet(instance=requerimiento, prefix='piezadetalle') # <<<< ASEGURA QUE ES 'piezadetalle'
    
    context = {
        'form': form,
        'servicio_detalle_formset': servicio_detalle_formset,
        'pieza_detalle_formset': pieza_detalle_formset,
        'requerimiento': requerimiento, 
        'modo': modo
    }
    return render(request, 'requerimiento/gestion.html', context)

@login_required
def borrar_requerimiento(request, id):
    requerimiento = get_object_or_404(Requerimiento, id=id)
    # if request.method == 'POST':
    requerimiento.delete()
    messages.success(request, 'Requerimiento (TDR) eliminado exitosamente.')
    return redirect('lista_requerimientos') 


# ¡REINTRODUCIDO!: API para buscar descripciones de servicio (para Select2)
@login_required
def buscar_descripcion_servicio_api(request):
    """
    Vista API para buscar descripciones de servicio existentes (para Select2)
    desde el catálogo LOCAL de 'requerimientos'.
    """
    query = request.GET.get('q', '')
    if query:
        # Aquí usa el campo 'descripcion_servicio' del modelo DescripcionServicio local
        descripciones = DescripcionServicio.objects.filter(descripcion_servicio__icontains=query)[:10]
        results = [{'id': d.id, 'text': d.descripcion_servicio} for d in descripciones]
    else:
        results = []
    return JsonResponse({'results': results})

# ¡REINTRODUCIDO!: API para crear una nueva descripción de servicio
@login_required
def crear_descripcion_servicio_api(request):
    """
    Vista API para crear una nueva descripción de servicio si no existe,
    en el catálogo LOCAL de 'requerimientos'.
    """
    if request.method == 'POST':
        descripcion_texto = request.POST.get('descripcion', '').strip()
        if descripcion_texto:
            try:
                # Aquí usa el campo 'descripcion_servicio' del modelo DescripcionServicio local
                descripcion_obj, created = DescripcionServicio.objects.get_or_create(
                    descripcion_servicio__iexact=descripcion_texto,
                    defaults={'descripcion_servicio': descripcion_texto}
                )
                return JsonResponse({'id': descripcion_obj.id, 'text': descripcion_obj.descripcion_servicio, 'created': created})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido o descripción vacía'}, status=400)

@login_required
def buscar_piezas_api(request):
    query = request.GET.get('q', '')
    if query:
        piezas = PiezaTDR.objects.filter(descripcion_pieza__icontains=query)[:10]
        results = [{'id': p.id, 'text': p.descripcion_pieza} for p in piezas]
    else:
        results = []
    return JsonResponse({'results': results})

@login_required
def crear_piezas_api(request):
    if request.method == 'POST':
        descripcion_pieza = request.POST.get('pieza', '').strip()
        if descripcion_pieza:
            try:
                descripcion_obj, created = PiezaTDR.objects.get_or_create(
                    descripcion_pieza__iexact=descripcion_pieza,
                    defaults={'descripcion_pieza': descripcion_pieza}
                )
                return JsonResponse({'id': descripcion_obj.id, 'text': descripcion_obj.descripcion_pieza, 'created': created})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido o pieza vacía'}, status=400)




class TDRPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Configurar márgenes: izquierdo=55mm, superior=15mm, derecho=15mm
        self.set_margins(left=55, top=15, right=15)
        self.set_auto_page_break(auto=True, margin=15)  # Margen inferior de 50mm
    
    def header(self):
        # HEADER - No afectado por el margen izquierdo de 55mm
        # Guardar posición actual
        original_x = self.get_x()
        original_y = self.get_y() + 26
        
        # Temporalmente resetear margen izquierdo para header centrado
        self.set_left_margin(15)
        self.set_x(15)  # Posicionar en el margen estándar
        
        if self.page_no() == 1:
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "TÉRMINOS DE REFERENCIA PARA SERVICIO DE MANTENIMIENTO", 0, 1, 'C')
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "ANEXO 'A': DESCRIPCIÓN Y CANTIDAD DEL SERVICIO A CONTRATAR", 0, 1, 'C')
            self.ln(4)
        else:
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "TÉRMINOS DE REFERENCIA PARA SERVICIO DE MANTENIMIENTO", 0, 1, 'C')
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "ANEXO 'A': DESCRIPCIÓN Y CANTIDAD DEL SERVICIO A CONTRATAR", 0, 1, 'C')
            self.ln(5)
        
        try:
            # sello_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'sello.png')
            sello_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'sello.jpg')
            # Posición relativa: 10mm desde izquierda, 20mm desde top
            self.image(sello_path, x=10, y=150, w=25, h=25)
        except Exception as e:
            self.set_xy(10, 150)
            self.set_font("Arial", "B", 10)
            self.cell(20, 20, "[SELLO]", 1, 0, 'C')
            print(f"Error al cargar el sello: {e}")


        # Restaurar margen izquierdo a 55mm y posición original
        self.set_left_margin(55)
        self.set_x(original_x)
        self.set_y(original_y)

    
    def footer(self):
        # FOOTER con sello agrandado a la derecha
        # Guardar posición Y actual
        original_y = self.get_y()
        
        # Posicionar a 35mm del fondo (dentro del margen inferior de 50mm)
        self.set_y(-25)
        
        # PRIMERA FILA: Información institucional a la izquierda
        self.set_font("Arial", "", 9)
        self.set_x(55)  # Alineado al margen izquierdo de 55mm
        
        # Posicionar el sello a la derecha (6.3cm ancho, 3.6cm alto)
        try:
            firma_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'firma.png')
            # Posición: x=130mm (para alinear a la derecha), y=posición actual
            self.image(firma_path, x=130, y=self.get_y(), w=40, h=15)  # 6.3cm x 3.6cm
            self.set_xy(180, -15)
            self.set_fill_color(0, 0, 0)     # Negro (RGB)
            self.set_text_color(255, 255, 255)  # Blanco
            self.set_font("Arial", "B", 12)  # Fuente en negrita
            self.cell(5, 5, f'{self.page_no()}', border=1, ln=0, align='C', fill=True)
        except Exception as e:
            # Texto alternativo si no se encuentra la imagen
            self.set_x(130)
            self.set_font("Arial", "B", 10)
            self.cell(63, 36, "[Firma]", 1, 0, 'C')
            print(f"Error al cargar la Firma: {e}")
        
        self.set_text_color(0, 0, 0)     # Texto negro
        self.set_fill_color(255, 255, 255)  # Fondo blanco
        
        # Restaurar posición Y original
        self.set_y(original_y)

@login_required
def generar_tdr_pdf(request, id):
    requerimiento = Requerimiento.objects.get(id=id)
    
    pdf = TDRPDF()
    pdf.add_page()
    
    # CONTENIDO PRINCIPAL (con margen izquierdo de 55mm)
    if pdf.page_no() == 1:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "VEHÍCULO 1:", 0, 1)
        
        pdf.set_font("Arial", "", 11)
        texto_vehiculo = (
            f"El presente requerimiento se realiza conforme al Informe Técnico Nro. "
            f"{requerimiento.informe_tecnico_nro}-REGPOL LL/UNIADM-AREABAST-A.M. de la Camioneta PNP de placa interna "
            f"{requerimiento.vehiculo.placa_int} placa de rodaje {requerimiento.vehiculo.placa_rod}, "
            f"Marca {requerimiento.vehiculo.marca}, Modelo {requerimiento.vehiculo.modelo}, "
            f"Motor N° {requerimiento.vehiculo.num_motor}, Serie Nro. {requerimiento.vehiculo.vin}, "
            f"Año {requerimiento.vehiculo.anio}, combustible {requerimiento.vehiculo.get_tipo_combustible_display()}, "
            f"asignado a la {requerimiento.vehiculo.subunidad.nombre}, dicho vehículo policial "
            f"para mejorar su operatividad requiere mantenimiento correctivo conforme a lo siguiente:"
        )
        
        pdf.multi_cell(0, 5, texto_vehiculo)
        pdf.ln(5)
        
        # Servicios
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "SERVICIO PARA REALIZAR", 0, 1)
        pdf.set_font("Arial", "", 11)
        
        
        for servicio in requerimiento.detalles_servicio.all():
            x = pdf.get_x()
            y = pdf.get_y()

            pdf.multi_cell(5, 6, "-", align="C")
            pdf.set_xy(x + 5, y)

            pdf.multi_cell(130, 6, servicio.detalle_servicio.descripcion_servicio )
            pdf.ln(0)
        
        pdf.ln(5)

        # Repuestos
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "CAMBIO E INSTALACIÓN DE LOS SIGUIENTES REPUESTOS", 0, 1)
    
    # Lista de repuestos
    pdf.set_font("Arial", "", 11)
    for repuesto in requerimiento.detalles_pieza.all():
        # Verificar si necesita nueva página (considerando margen inferior de 50mm)
        if pdf.get_y() > 260:
            pdf.add_page()
        x = pdf.get_x()
        y = pdf.get_y()

        pdf.multi_cell(3, 5, "-", align="C")
        pdf.set_xy(x + 5, y)
        # SOLUCIÓN: Verifica que detalle_pieza no sea None
        if repuesto.detalle_pieza:
            pieza_texto = repuesto.detalle_pieza.descripcion_pieza
        else:
            pieza_texto = "[Pieza eliminada]"
        pdf.multi_cell(120, 5, f"{repuesto.cantidad} {pieza_texto}" )

    # Generar respuesta PDF
    response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="tdr_vehiculo_{requerimiento.id}.pdf"'
    return response

@login_required
def generar_consolidado_tdr_pdf(request):
    ids_list = request.GET.getlist('ids')
    ids_list = ids_list[0].split(',')
    start_page = int(request.GET.get('start_page', '1') or request.POST.get('start_page', '1'))
    ids = [int(i) for i in ids_list if str(i).isdigit()]
    if not ids:
        messages.error(request, "No se seleccionaron TDRs válidos.")
        return redirect('lista_consolidados')
    requerimientos = Requerimiento.objects.filter(id__in=ids).select_related('vehiculo', 'vehiculo__subunidad').prefetch_related(
        'detalles_servicio__detalle_servicio',
        'detalles_pieza__detalle_pieza'
    ).order_by('id')

    # Solo crear el registro si viene del formulario de selección (POST o no existe un consolidado igual)
    if request.method == "POST" or not ConsolidadoTDR.objects.filter(start_page=start_page, tdrs__in=requerimientos).exists():
        consolidado = ConsolidadoTDR.objects.create(start_page=start_page)
        consolidado.tdrs.set(requerimientos)
    # Si es GET y ya existe, no crear nada

    pdf = TDRPDF()
    pdf.add_page()
    pdf.page_no_override = start_page - 1

    def page_no_custom(self):
        return self.page_no_override + super(TDRPDF, self).page_no()
    pdf.page_no = page_no_custom.__get__(pdf, TDRPDF)

    vehiculo_num = 1
    for requerimiento in requerimientos:
        # Si el contenido se acerca al final de la página, agrega una nueva página
        if pdf.get_y() > 220:  # Puedes ajustar este valor según tu formato
            pdf.add_page()

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"VEHÍCULO {vehiculo_num}:", 0, 1)

        pdf.set_font("Arial", "", 11)
        texto_vehiculo = (
            f"El presente requerimiento se realiza conforme al Informe Técnico Nro. "
            f"{requerimiento.informe_tecnico_nro}-REGPOL LL/UNIADM-AREABAST-A.M. de la Camioneta PNP de placa interna "
            f"{requerimiento.vehiculo.placa_int} placa de rodaje {requerimiento.vehiculo.placa_rod}, "
            f"Marca {requerimiento.vehiculo.marca}, Modelo {requerimiento.vehiculo.modelo}, "
            f"Motor N° {requerimiento.vehiculo.num_motor}, Serie Nro. {requerimiento.vehiculo.vin}, "
            f"Año {requerimiento.vehiculo.anio}, combustible {requerimiento.vehiculo.get_tipo_combustible_display()}, "
            f"asignado a la {requerimiento.vehiculo.subunidad.nombre}, dicho vehículo policial "
            f"para mejorar su operatividad requiere mantenimiento correctivo conforme a lo siguiente:"
        )
        pdf.multi_cell(0, 5, texto_vehiculo)
        pdf.ln(5)

        # Servicios
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "SERVICIO PARA REALIZAR", 0, 1)
        pdf.set_font("Arial", "", 11)
        for servicio in requerimiento.detalles_servicio.all():
            if pdf.get_y() > 260:
                pdf.add_page()
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.multi_cell(5, 6, "-", align="C")
            pdf.set_xy(x + 5, y)
            if servicio.detalle_servicio:
                pdf.multi_cell(130, 6, servicio.detalle_servicio.descripcion_servicio)
            else:
                pdf.multi_cell(130, 6, "[Servicio eliminado]")
            pdf.ln(0)
        pdf.ln(5)

        # Repuestos
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "CAMBIO E INSTALACIÓN DE LOS SIGUIENTES REPUESTOS", 0, 1)
        pdf.set_font("Arial", "", 11)
        for repuesto in requerimiento.detalles_pieza.all():
            if pdf.get_y() > 260:
                pdf.add_page()
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.multi_cell(3, 5, "-", align="C")
            pdf.set_xy(x + 5, y)
            if repuesto.detalle_pieza:
                pieza_texto = repuesto.detalle_pieza.descripcion_pieza
            else:
                pieza_texto = "[Pieza eliminada]"
            pdf.multi_cell(120, 5, f"{repuesto.cantidad} {pieza_texto}")
        pdf.ln(10)  # Espacio entre TDRs

        vehiculo_num += 1

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tdr_consolidado.pdf"'
    return response

@login_required
def consolidado_tdr_seleccion(request):
    # Solo TDRs que no están en ningún consolidado
    requerimientos = Requerimiento.objects.filter(consolidados=None).select_related('vehiculo').order_by('-fecha_creacion')
    requerimientos = paginacion(request, requerimientos)
    return render(request, 'requerimiento/consolidado.html', {
        'requerimientos': requerimientos,
    })

@login_required
def lista_consolidados(request):
    search = request.GET.get('search', '').strip()
    consolidados = ConsolidadoTDR.objects.all().order_by('-fecha')
    if search:
        consolidados = consolidados.filter(
            tdrs__informe_tecnico_nro__icontains=search
        ).distinct()
    consolidados = paginacion(request, consolidados)
    return render(request, 'requerimiento/lista_consolidados.html', {
        'consolidados': consolidados,
        'urlindex': 'lista_consolidados', 
        'urlcrear': 'consolidado_tdr_seleccion', 
    })

@login_required
def consolidado_tdr_borrar(request, id):
    consolidado = get_object_or_404(ConsolidadoTDR, id=id)
    consolidado.delete()
    messages.success(request, "Consolidado eliminado correctamente.")
    return redirect('lista_consolidados')

@login_required
def crear_consolidado_tdr(request):
    if request.method == "POST":
        ids_list = request.POST.getlist('ids')
        start_page = int(request.POST.get('start_page', '1'))
        ids = [int(i) for i in ids_list if str(i).isdigit()]
        if not ids:
            messages.error(request, "No se seleccionaron TDRs válidos.")
            return redirect('consolidado_tdr_seleccion')
        requerimientos = Requerimiento.objects.filter(id__in=ids)
        consolidado = ConsolidadoTDR.objects.create(start_page=start_page)
        consolidado.tdrs.set(requerimientos)
        messages.success(request, "Consolidado creado correctamente.")
        return redirect('lista_consolidados')
    else:
        return redirect('consolidado_tdr_seleccion')