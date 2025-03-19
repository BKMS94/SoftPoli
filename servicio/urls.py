from django.urls import path
from . import views

urlpatterns = [
    path('', views.servicio_lista, name='servicio_lista'),
    path('crear/', views.servicio_crear, name='servicio_crear'),
    path('<int:id>/', views.servicio_detalle, name='servicio_detalle'),
    path('editar/<int:id>/', views.servicio_editar, name='servicio_editar'),
    path('borrar/<int:id>/', views.servicio_borrar, name='servicio_borrar'),
    path('movimientos/', views.movimiento_lista, name='movimiento_lista'),
    path('movimientos/crear/', views.movimiento_crear, name='movimiento_crear'),
    path('movimientos/<int:id>/', views.movimiento_detalle, name='movimiento_detalle'),
    path('movimientos/editar/<int:id>/', views.movimiento_editar, name='movimiento_editar'),
    path('movimientos/borrar/<int:id>/', views.movimiento_borrar, name='movimiento_borrar'),
]