from django.urls import path
from . import views


urlpatterns = [
    path('', views.comisaria_lista, name='comisaria_index'),
    path('crear/', views.comisaria_gestion, name='comisaria_crear'),
    path('editar/<int:id>/', views.comisaria_gestion, name='comisaria_editar'),
    path('<int:id>/', views.comisaria_detalle, name='comisaria_detalle'),
    path('borrar/<int:pk>/', views.comisaria_borrar, name='comisaria_borrar'),
]