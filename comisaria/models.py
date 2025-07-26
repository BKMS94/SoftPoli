from django.db import models
from django.urls import reverse
from persona.models import Persona

class Comisaria(models.Model):

    nombre = models.CharField(
        max_length= 50,
        verbose_name= 'Nombre de la comisaría'
    )
    direccion = models.CharField(
        max_length= 70,
        verbose_name= 'Dirección'
    )
    telefono_contacto = models.PositiveIntegerField(
        default=000000000,
        max_length=9,
        blank=True,
        null=True
    )
    responsable = models.ForeignKey(
        Persona, on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Comisaria'
        verbose_name_plural = 'Comisarias'

    
    def __str__(self):
        return self.nombre
    
    def get_detalle_url(self):
        return reverse('comisaria_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('comisaria_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('comisaria_borrar', args=[self.id])
