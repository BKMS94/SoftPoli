from django.db import models
from django.urls import reverse


# Create your models here.

class Vehiculo(models.Model):
    placa = models.CharField(max_length=6, blank= None)
    marca = models.CharField(max_length=50, blank= None)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField(blank= None)
    kilometraje = models.IntegerField(blank=None)
    created = models.DateTimeField(editable=None, auto_now=True)

    def __str__(self):
        return self.placa

    def get_detalle_url(self):
        return reverse('vehiculo_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('vehiculo_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('vehiculo_borrar', args=[self.id])
    