from django.urls import path
from . import views

urlpatterns = [
    # URLs CRUD para Requerimientos
    path('', views.lista_requerimientos, name='lista_requerimientos'),
    path('crear/', views.requerimiento_form, name='crear_requerimiento'),
    path('<int:pk>/', views.detalle_requerimiento, name='detalle_requerimiento'),
    path('<int:pk>/editar/', views.requerimiento_form, name='editar_requerimiento'),
    path('<int:pk>/borrar/', views.borrar_requerimiento, name='borrar_requerimiento'),

    # URL para generar el PDF del TDR
    path('<int:pk>/generar-pdf/', views.generar_tdr_pdf, name='generar_tdr_pdf'),

    # URLs API para autocompletado y creación (si las mueves aquí desde 'servicios')
    path('api/descripciones/buscar/', views.buscar_descripcion_servicio_api, name='buscar_descripcion_servicio_api'),
    path('api/descripciones/crear/', views.crear_descripcion_servicio_api, name='crear_descripcion_servicio_api'),
    path('api/piezas/buscar/', views.buscar_piezas_api, name='buscar_piezas_api'),
]
