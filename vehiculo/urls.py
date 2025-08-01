from django.urls import path
from . import views

urlpatterns=[
    path('', views.vehiculo_lista, name='vehiculo_index'),
    path('crear/', views.vehiculo_gestion, name='vehiculo_crear'),
    path('<int:id>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('editar/<int:id>/', views.vehiculo_gestion, name='vehiculo_editar'),
    path('borrar/<int:id>/', views.vehiculo_borrar, name='vehiculo_borrar'), 
    path('kilometraje/<int:id>/', views.vehiculo_kilometraje, name='vehiculo-kilometraje'),
]