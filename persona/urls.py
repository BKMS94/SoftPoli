from django.urls import path
from . import views

urlpatterns = [
    path('persona/', views.persona_index, name='persona_index'),
    path('persona/crear/', views.persona_gestion, name='persona_crear'),
    path('persona/<int:id>/', views.persona_detalle, name='persona_detalle'),
    path('persona/editar/<int:id>/', views.persona_gestion, name='persona_editar'),
    path('persona/borrar/<int:id>/', views.persona_borrar, name='persona_borrar'),
    path('tecnico/', views.tecnico_index, name='tecnico_index'),
    path('tecnico/crear/', views.tecnico_gestion, name='tecnico_crear'),
    path('tecnico/<int:id>/', views.tecnico_detalle, name='tecnico_detalle'),
    path('tecnico/editar/<int:id>/', views.tecnico_gestion, name='tecnico_editar'),
    path('tecnico/borrar/<int:id>/', views.tecnico_borrar, name='tecnico_borrar'),

]