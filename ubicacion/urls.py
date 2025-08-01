from django.urls import path
from . import views


urlpatterns = [
    path('subunidad/', views.subunidad_lista, name='subunidad_index'),
    path('subunidad/crear/', views.subunidad_gestion, name='subunidad_crear'),
    path('subunidad/editar/<int:id>/', views.subunidad_gestion, name='subunidad_editar'),
    path('subunidad/<int:id>/', views.subunidad_detalle, name='subunidad_detalle'),
    path('subunidad/borrar/<int:id>/', views.subunidad_borrar, name='subunidad_borrar'),
    path('unidad/', views.unidad_lista, name='unidad_index'),
    path('unidad/crear/', views.unidad_gestion, name='unidad_crear'),
    path('unidad/editar/<int:id>/', views.unidad_gestion, name='unidad_editar'),
    path('unidad/<int:id>/', views.unidad_detalle, name='unidad_detalle'),
    path('unidad/borrar/<int:id>/', views.unidad_borrar, name='unidad_borrar'),
    path('unidad-autocomplete/', views.UnidadAutocomplete.as_view(), name='unidad-autocomplete'),
]