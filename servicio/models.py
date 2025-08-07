from django.db import models
from django.urls import reverse
from vehiculo.models import Vehiculo
from persona.models import Persona,Tecnico
from pieza.models import Pieza
# Create your models here.

TIPO_MANTENIMIENTO_CHOICES = [
    ('Correctivo', 'Correctivo'),
    ('Preventivo', 'Preventivo')
    ]

class Servicio(models.Model):
    fecha = models.DateTimeField(editable=False, auto_now=True)
    descripcion = models.TextField(null=False, blank=False)
    kilometraje_ant = models.DecimalField(max_digits= 18,
        decimal_places=1,
        blank=False,
        null=False,)
    kilometraje_act = models.DecimalField(max_digits= 18,
        decimal_places=1,
        blank=False,
        null=False,)
    kilometraje_diff = models.DecimalField(max_digits= 18,
        decimal_places=1,
        blank=False,
        null=False,)
    tipo = models.TextField(choices=TIPO_MANTENIMIENTO_CHOICES, default='Preventivo')
    vehiculo = models.ForeignKey(Vehiculo, on_delete= models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio {self.id} - {self.vehiculo.placa_int}"

    def get_detalle_url(self):
        return reverse('servicio_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('servicio_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('servicio_borrar', args=[self.id])
    
    
class Descripcion_Servicio(models.Model):
    descripcion = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Descripcion_Servicio {self.id} - {self.vehiculo.placa_int}"

    def get_detalle_url(self):
        return reverse('descripcion_Servicio_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('descripcion_Servicio_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('descripcion_Servicio_borrar', args=[self.id])

class MovimientoStock(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(editable=None, auto_now=True)
    

    def __str__(self):
        return f"{self.cantidad} x {self.pieza.nombre} en Servicio {self.servicio.id}"



class Aaddservicios(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    descripcion_servicio = models.ForeignKey(Descripcion_Servicio, on_delete=models.CASCADE)
