from django.urls import path
from . import views

urlpatterns = [
    # URLs CRUD para Requerimientos
    path('', views.requerimiento_lista, name='lista_requerimientos'),
    path('crear/', views.requerimiento_form, name='crear_requerimiento'),
    path('<int:id>/', views.detalle_requerimiento, name='detalle_requerimiento'),
    path('<int:id>/editar/', views.requerimiento_form, name='editar_requerimiento'),
    path('<int:id>/borrar/', views.borrar_requerimiento, name='borrar_requerimiento'),

    # URL para generar el PDF del TDR
    path('<int:id>/generar-pdf/', views.generar_tdr_pdf, name='generar_tdr_pdf'),
    path('consolidado/', views.consolidado_tdr_seleccion, name='consolidado_tdr_seleccion'),
    path('consolidado-pdf/', views.generar_consolidado_tdr_pdf, name='generar_consolidado_tdr_pdf'),

    # ¡ELIMINADO!: URLs API para autocompletado y creación de Descripciones de Servicio.
    path('api/descripciones/buscar/', views.buscar_descripcion_servicio_api, name='buscar_descripcion_servicio_api'),
    path('api/descripciones/crear/', views.crear_descripcion_servicio_api, name='crear_descripcion_servicio_api'),
    path('api/piezas/buscar/', views.buscar_piezas_api, name='buscar_piezas_api'),
    path('api/piezas/crear/', views.crear_piezas_api, name='crear_piezas_api'),

    # URL para el detalle del requerimiento en formato de modal (snippet HTML)
    path('<int:id>/modal-detalle/', views.detalle_requerimiento_modal, name='detalle_requerimiento_modal'),

    # Nueva URL para la lista de consolidados
    path('consolidados/', views.lista_consolidados, name='lista_consolidados'),
]
