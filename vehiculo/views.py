from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.http import JsonResponse
from maestranza.utils import paginacion,modo_gestion
from .models import Vehiculo
from .forms import VehiculoForm,VehiculoImportForm
from django.contrib.auth.decorators import login_required
import pandas as pd
from ubicacion.models import Unidad, SubUnidad
from django.db import transaction

# Create your views here.

@login_required
def vehiculo_lista(request):
    vehiculos = Vehiculo.objects.filter(placa_int__icontains= request.GET.get('search', '')).order_by('id') 
    vehiculos = paginacion(request,vehiculos)
    context = {
        'vehiculos': vehiculos,
        'urlindex': 'vehiculo_index',
        'urlcrear': 'vehiculo_crear',
        'request': request,  
    }
    return render(request, 'vehiculo/index.html', context)


@login_required
def vehiculo_gestion(request, id=None):
    vehiculos, modo, extra = modo_gestion(Vehiculo,id)

    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculos)
        if form.is_valid():
            try:
                vehiculos = form.save()
                messages.success(request, f"Vehículo {'creado' if modo == 'crear' else 'actualizado'} correctamente.")
                return redirect('vehiculo_index')
            except Exception as e:
                messages.error(request, f"Error al guardar el vehículos: {e}")
    else:
        form = VehiculoForm(instance=vehiculos)
    context = {
        'form' : form,
        'vehiculos': vehiculos,
        'modo': modo,
        'extra': extra
    }
    return render(request, 'vehiculo/gestion.html', context)


@login_required
def vehiculo_detalle(request,id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    context = {'vehiculo':vehiculo}
    return render(request, 'vehiculo/detalle.html', context)


@login_required
def vehiculo_borrar(request,id):
    vehiculo = get_object_or_404(Vehiculo, id=id)
    vehiculo.delete()
    return redirect('vehiculo_index')

# @login_required
def vehiculo_kilometraje(request, id):
    try:
        vehiculo = get_object_or_404(Vehiculo, id=id)
        kilometraje = vehiculo.kilometraje  # Ajusta el nombre del campo si es diferente
    except Vehiculo.DoesNotExist:
        kilometraje = 0
    return JsonResponse({'kilometraje': kilometraje})

@login_required
def vehiculo_importar(request):
    if request.method == 'POST':
        form = VehiculoImportForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']
            try:
                df = pd.read_excel(archivo, header=0)
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                df.columns = df.columns.str.strip()
                df.rename(columns={
                    'N°': 'id',
                    'MARCA':'marca',
                    'MODELO': 'modelo',
                    'AÑO': 'anio',
                    'TIPO DE VEHICULO':'tipo',
                    'TIPO DE COMBUSTIBLE': 'tipo_combustible',
                    'Nº DE SERIE': 'vin',
                    'ESTADO DEL ODOMETRO': 'estado_odo',
                    'ESTADO DEL VEHICULO': 'estado_vehi',
                    'Nº DE  MOTOR': 'num_motor',
                    'PLACA INTERNA': 'placa_int',
                    'PLACA RODAJE': 'placa_rod',
                    'FUNCION POLICIAL': 'funcion',
                    'UNIDAD': 'unidad',
                    'SUB UNIDAD': 'subunidad',
                    'PROCEDENCIA' : 'procedencia',
                    'MOTIVO O CAUSA DE LA INOPERATIVIDAD': 'motivo_ino',
                    'FECHA DE LA INOPERATIVIDAD':'fecha_ino',
                    'UBICACIÓN': 'ubicacion_ino',
                    'NRO. RESOLUCION DE BAJA': 'resolucion_baja',
                    'FECHA RD BAJA': 'fecha_baja'
                }, inplace=True)

                # Asegura columnas requeridas
                for col in ['placa_int', 'subunidad', 'unidad']:
                    if col not in df.columns:
                        messages.error(request, f"Falta la columna '{col}' en el archivo.")
                        return render(request, 'vehiculo/importar.html', {'form': form})

                # Agrega columnas faltantes con valores por defecto
                for col in ['fecha_adquisicion', 'kilometraje', 'valor', 'fecha_ino', 'motivo_ino', 'ubicacion_ino', 'resolucion_baja', 'fecha_baja']:
                    if col not in df.columns:
                        df[col] = None

                # Limpieza y normalización
                df['estado_odo'] = df['estado_odo'].apply(lambda x: 'OPERATIVO' if str(x).startswith('OPERAT') else 'INOPERATIVO')
                df['funcion'] = df['funcion'].apply(lambda x: 'ADMINISTRATIVO' if x == 'ADMINISTRAT.' else x)
                df['kilometraje'] = df['kilometraje'].fillna(0)
                df['valor'] = df['valor'].fillna(0)

                # Formatea fechas
                def parse_fecha(valor):
                    try:
                        return pd.to_datetime(valor, errors='coerce')
                    except Exception:
                        return None
                for col in ['fecha_adquisicion', 'fecha_ino', 'fecha_baja']:
                    if col in df.columns:
                        df[col] = df[col].apply(parse_fecha)

                # Elimina duplicados por placa_int
                df = df.drop_duplicates(subset=['placa_int'], keep='first')
                df = df.drop_duplicates(subset=['placa_rod'], keep='first')
                df = df.drop_duplicates(subset=['vin'], keep='first')

                # Procesa UNIDADES
                unidades = df['unidad'].dropna().unique()
                unidad_objs = {}
                for nombre in unidades:
                    nombre_str = str(nombre).strip()
                    if not nombre_str or nombre_str.lower() == 'nan':
                        continue
                    obj, _ = Unidad.objects.get_or_create(nombre=nombre_str)
                    unidad_objs[nombre_str] = obj

                # Junta subunidad y ubicacion_ino en una sola serie
                subunidad_col = df['subunidad'].dropna().astype(str).str.strip()
                ubicacion_ino_col = df['ubicacion_ino'].dropna().astype(str).str.strip()
                todas_subunidades = pd.concat([subunidad_col, ubicacion_ino_col]).drop_duplicates()
                todas_subunidades = todas_subunidades[todas_subunidades != '']

                # Crea todas las subunidades posibles
                subunidad_objs = {}
                for nombre in todas_subunidades:
                    nombre_str = str(nombre).strip()
                    if not nombre_str or nombre_str.lower() == 'nan':
                        continue
                    # Busca la unidad asociada (primera ocurrencia en el DataFrame)
                    unidad_nombre = df[df['subunidad'] == nombre_str]['unidad'].dropna().astype(str).str.strip().head(1)
                    unidad_obj = unidad_objs.get(unidad_nombre.iloc[0]) if not unidad_nombre.empty else None
                    obj, _ = SubUnidad.objects.get_or_create(nombre=nombre_str, defaults={'unidad': unidad_obj})
                    if obj.unidad != unidad_obj and unidad_obj is not None:
                        obj.unidad = unidad_obj
                        obj.save()
                    subunidad_objs[nombre_str] = obj

                # Detecta duplicados en placa_rod y vin en el Excel
                duplicados_placa_rod = df[df.duplicated(subset=['placa_rod'], keep=False) & df['placa_rod'].notna()]
                duplicados_vin = df[df.duplicated(subset=['vin'], keep=False) & df['vin'].notna()]

                if not duplicados_placa_rod.empty or not duplicados_vin.empty:
                    msg = []
                    if not duplicados_placa_rod.empty:
                        msg.append("Placas rodaje duplicadas en el archivo: " + ", ".join(duplicados_placa_rod['placa_rod'].unique()))
                    if not duplicados_vin.empty:
                        msg.append("VIN duplicados en el archivo: " + ", ".join(duplicados_vin['vin'].unique()))
                    messages.error(request, " ".join(msg))
                    return render(request, 'vehiculo/importar.html', {'form': form})

                errores = []
                with transaction.atomic():
                    for _, row in df.iterrows():
                        placa_int = str(row['placa_int']).strip()
                        if not placa_int:
                            continue
                        subunidad = subunidad_objs.get(str(row['subunidad']).strip()) if row['subunidad'] else None
                        ubicacion_ino = subunidad_objs.get(str(row['ubicacion_ino']).strip()) if 'ubicacion_ino' in row and row['ubicacion_ino'] else None
                        
                        # Antes de update_or_create
                        placa_rod = str(row.get('placa_rod', '') or '')
                        vin = str(row.get('vin', '') or '')

                        if placa_rod:
                            existe_placa_rod = Vehiculo.objects.filter(placa_rod=placa_rod).exclude(placa_int=placa_int).exists()
                            if existe_placa_rod:
                                errores.append(f"{placa_int}: placa_rod '{placa_rod}' ya existe en otro vehículo.")
                                continue

                        if vin:
                            existe_vin = Vehiculo.objects.filter(vin=vin).exclude(placa_int=placa_int).exists()
                            if existe_vin:
                                errores.append(f"{placa_int}: vin '{vin}' ya existe en otro vehículo.")
                                continue

                        try:
                            vehiculo, creado = Vehiculo.objects.update_or_create(
                                placa_int=placa_int,
                                defaults={
                                    'placa_rod': str(row.get('placa_rod', '') or ''),
                                    'vin': str(row.get('vin', '') or ''),
                                    'num_motor': str(row.get('num_motor', '') or ''),
                                    'marca': str(row.get('marca', '') or ''),
                                    'modelo': str(row.get('modelo', '') or ''),
                                    'anio': int(row.get('anio', 2000)) if pd.notna(row.get('anio', 2000)) else 2000,
                                    'tipo': str(row.get('tipo', '') or ''),
                                    'kilometraje': int(row.get('kilometraje', 0)) if pd.notna(row.get('kilometraje', 0)) else 0,
                                    'estado_vehi': str(row.get('estado_vehi', 'OPERATIVO') or 'OPERATIVO'),
                                    'estado_odo': str(row.get('estado_odo', 'OPERATIVO') or 'OPERATIVO'),
                                    'fecha_adquisicion': safe_date(row.get('fecha_adquisicion', None)),
                                    'tipo_combustible': str(row.get('tipo_combustible', '') or ''),
                                    'procedencia': str(row.get('procedencia', '') or ''),
                                    'funcion': str(row.get('funcion', 'ADMINISTRATIVO') or 'ADMINISTRATIVO'),
                                    'valor': float(row.get('valor', 0)) if pd.notna(row.get('valor', 0)) else 0,
                                    'subunidad': subunidad,
                                    'motivo_ino': str(row.get('motivo_ino', '') or ''),
                                    'fecha_ino': safe_date(row.get('fecha_ino', None)),
                                    'ubicacion_ino': ubicacion_ino,
                                    'resolucion_baja': str(row.get('resolucion_baja', '') or ''),
                                    'fecha_baja': safe_date(row.get('fecha_baja', None)),
                                }
                            )
                        except Exception as e:
                            errores.append(f"{placa_int}: {e}")
                if errores:
                    messages.warning(request, "Algunos vehículos no se importaron: " + "; ".join(errores))
                else:
                    messages.success(request, "Archivo procesado y datos importados/actualizados correctamente.")
                return redirect('vehiculo_index')
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")
    else:
        form = VehiculoImportForm()
    return render(request, 'vehiculo/importar.html', {'form': form})

def safe_date(val):
    if pd.isna(val):
        return None
    return val