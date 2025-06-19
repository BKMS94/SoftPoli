from django.db import models
from django.urls import reverse


# Create your models here.

class Vehiculo(models.Model):
    placa = models.CharField(
        max_length=6,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Placa",
        help_text="Placa única del vehículo"
    )
    marca = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name="Marca"
    )
    modelo = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name="Modelo"
    )
    anio = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Año"
    )
    kilometraje = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Kilometraje"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    def __str__(self):
        return self.placa

    def get_detalle_url(self):
        return reverse('vehiculo_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('vehiculo_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('vehiculo_borrar', args=[self.id])
