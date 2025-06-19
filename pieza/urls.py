from django.urls import path
from . import views

urlpatterns=[
    path('', views.pieza_lista, name='pieza_index'),
    path('crear/', views.pieza_crear, name='pieza_crear'),
    path('<int:id>/', views.pieza_detalle, name='pieza_detalle'),
    path('editar/<int:id>/', views.pieza_editar, name='pieza_editar'),
    path('borrar/<int:id>/', views.pieza_borrar, name='pieza_borrar'), 
    path('stock/<int:pieza_id>/', views.pieza_stock, name='pieza_stock'),
]