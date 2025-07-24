from django.urls import path
from . import views

urlpatterns = [
    # path('', views.servicio_lista, name='servicio_lista'),
    path('crear/', views.servicio_form, name='servicio_crear'),
    path('<int:id>/', views.servicio_detalle, name='servicio_detalle'),
    path('editar/<int:id>/', views.servicio_form, name='servicio_editar'),
    path('', views.servicio_lista, name='servicio_lista'),
    path('<int:pk>/', views.servicio_detalle, name='servicio_detalle'), # Asegúrate de que esta vista acepte 'pk'
    path('borrar/<int:pk>/', views.servicio_borrar, name='servicio_borrar'), # Asegúrate de que esta vista acepte 'pk'
    path('vehiculo-autocomplete/', views.VehiculoAutocomplete.as_view(), name='vehiculo-autocomplete'),
    path('persona-autocomplete/', views.PersonaAutocomplete.as_view(), name='persona-autocomplete'),
    path('tecnico-autocomplete/', views.TecnicoAutocomplete.as_view(), name='tecnico-autocomplete'),
    path('pieza-autocomplete/', views.PiezaAutocomplete.as_view(), name='pieza-autocomplete'),
    path('generar_pdf_servicio/<int:id>/', views.generar_pdf_servicio, name='generar_pdf_servicio'),

]