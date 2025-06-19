from django.db import models
from django.urls import reverse
from vehiculo.models import Vehiculo
from persona.models import Persona,Tecnico
from pieza.models import Pieza
# Create your models here.

class Servicio(models.Model):
    fecha = models.DateTimeField(editable=False, auto_now=True)
    descripcion = models.TextField(null=False, blank=False)
    kilometraje_act = models.PositiveIntegerField(default=0)
    kilometraje_diff = models.PositiveIntegerField(default=0)
    vehiculo = models.ForeignKey(Vehiculo, on_delete= models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio {self.id} - {self.vehiculo.placa}"

    def get_detalle_url(self):
        return reverse('servicio_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('servicio_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('servicio_borrar', args=[self.id])

class MovimientoStock(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(editable=None, auto_now=True)
    

    def __str__(self):
        return f"{self.cantidad} x {self.pieza.nombre} en Servicio {self.servicio.id}"

    
    def get_detalle_url(self):
        return reverse('movimiento_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('movimiento_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('movimiento_borrar', args=[self.id])
