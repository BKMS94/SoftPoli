from django.urls import path
from . import views

urlpatterns= [
    path('', views.grado_lista, name='grado_lista'),
    path('crear/', views.grado_crear, name='grado_crear'),
    path('<int:id>/', views.grado_detalle, name='grado_detalle'),
    path('editar/<int:id>/', views.grado_editar, name='grado_editar'),
    path('borrar/<int:id>/', views.grado_borrar, name='grado_borrar'),
]