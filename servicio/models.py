from django.db import models
from django.urls import reverse
from vehiculo.models import Vehiculo
from persona.models import Persona,Tecnico
from pieza.models import Pieza
from datetime import datetime
# Create your models here.

TIPO_MANTENIMIENTO_CHOICES = [
    ('CORRECTIVO', 'CORRECTIVO'),
    ('PREVENTIVO', 'PREVENTIVO')
    ]

ESTADO_SERVICIO_CHOICES=[
    ('EN PROCESO', 'En proceso'), 
    ('FINALIZADO', 'Finalizado')
    ]

class Servicio(models.Model):
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
    fecha_inicio = models.DateTimeField(editable=False, auto_now=False, default= datetime.now())
    fecha_fin = models.DateTimeField(editable=True, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_SERVICIO_CHOICES,
        default='EN PROCESO'
    )

    def __str__(self):
        return f"Servicio {self.id} - {self.vehiculo.placa_int}"

    def get_detalle_url(self):
        return reverse('servicio_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('servicio_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('servicio_borrar', args=[self.id])
    
    def get_fin_url(self):
        return reverse('finalizar_servicio', args=[self.id])
    
    def get_pdf_url(self):
        return reverse('generar_pdf_servicio', args=[self.id])
    
class MovimientoStock(models.Model):
    pieza = models.ForeignKey(Pieza, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(editable=None, auto_now=True)
    

    def __str__(self):
        return f"{self.cantidad} x {self.pieza.nombre} en Servicio {self.servicio.id}"
    
    
# class DescripcionServicio(models.Model):
#     """
#     Modelo para almacenar descripciones de servicios únicas y predefinidas.
#     """
#     descripcion = models.CharField(
#         max_length=255,
#         unique=True, # Asegura que no haya descripciones duplicadas
#         verbose_name="Descripción del Servicio"
#     )

#     class Meta:
#         verbose_name = "Descripción de Servicio"
#         verbose_name_plural = "Descripciones de Servicio"
#         ordering = ['descripcion']

#     def __str__(self):
#         return self.descripcion


# class ServicioDetalle(models.Model):
#     """
#     Modelo intermedio (through model) para la relación ManyToMany entre Servicio y DescripcionServicio.
#     Permite añadir múltiples descripciones a un servicio.
#     """
#     servicio = models.ForeignKey(
#         Servicio, 
#         on_delete=models.CASCADE,
#         verbose_name="Servicio Principal"
#     )
#     descripcion_servicio = models.ForeignKey(
#         DescripcionServicio, 
#         on_delete=models.CASCADE,
#         verbose_name="Descripción de la Tarea"
#     )
#     class Meta:
#         unique_together = ('servicio', 'descripcion_servicio') # Una tarea no se repite en el mismo servicio
#         verbose_name = "Detalle de Servicio"
#         verbose_name_plural = "Detalles de Servicio"

#     def __str__(self):
#         return f"{self.descripcion_servicio.descripcion} para Servicio {self.servicio.id}"

