from django.db import models
from django.urls import reverse
from persona.models import Persona


class Unidad(models.Model):
    nombre = models.CharField(
        max_length= 50,
        verbose_name= 'Nombre de la Sub Unidad'
    )

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nombre
    
    def get_detalle_url(self):
        return reverse('unidad_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('unidad_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('unidad_borrar', args=[self.id])


class SubUnidad(models.Model):

    nombre = models.CharField(
        max_length= 50,
        verbose_name= 'Nombre de la Sub Unidad'
    )
    direccion = models.CharField(
        max_length= 70,
        verbose_name= 'Dirección',
        blank=True,
        null=True
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
    unidad = models.ForeignKey(
        Unidad, on_delete= models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Sub Unidad'
        verbose_name_plural = 'Sub Unidades'

    
    def __str__(self):
        return self.nombre
    
    def get_detalle_url(self):
        return reverse('subunidad_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('subunidad_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('subunidad_borrar', args=[self.id])
