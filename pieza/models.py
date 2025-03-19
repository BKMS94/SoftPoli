from django.db import models
from django.urls import reverse

# Create your models here.

class Pieza(models.Model):
    nombre = models.CharField(max_length=100, blank=None)
    cantidad_stock = models.IntegerField()
    reorder = models.IntegerField()

    def __str__(self):
        return self.nombre

    def get_detalle_url(self):
        return reverse('pieza_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('pieza_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('pieza_borrar', args=[self.id])


