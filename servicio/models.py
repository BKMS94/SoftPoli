from django.db import models
from django.urls import reverse
from vehiculo.models import Vehiculo
from persona.models import Persona,Tecnico
from pieza.models import Pieza
# Create your models here.

class Servicio(models.Model):
    fecha = models.DateTimeField(editable=False, auto_now=True)
    descripcion = models.TextField(null=False, blank=False)
    kilometraje_act = models.IntegerField(default=0, null=False, blank=False)
    kilometraje_diff= models.IntegerField(default=0)
    costo = models.DecimalField(max_digits=12,decimal_places=2)
    vehiculo = models.ForeignKey(Vehiculo, on_delete= models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)

    def __str__(self):
        return self.vehiculo

    def get_detalle_url(self):
        return reverse('servicio_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('servicio_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('servicio_borrar', args=[self.id])

class MovimientoStock(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(editable=None, auto_now=True)
    

    def __str__(self):
        return self.pieza
    
    def get_detalle_url(self):
        return reverse('movimiento_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('movimiento_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('movimiento_borrar', args=[self.id])
