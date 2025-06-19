from django.db import models
from django.urls import reverse

class Pieza(models.Model):
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name="Nombre"
    )
    cantidad_stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock actual",
        help_text="Cantidad disponible en inventario"
    )
    reorder = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad de aviso",
        help_text="Cantidad mínima antes de avisar stock bajo"
    )

    def __str__(self):
        return self.nombre

    def get_detalle_url(self):
        return reverse('pieza_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('pieza_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('pieza_borrar', args=[self.id])

    def stock_bajo(self):
        """¿Está el stock por debajo del mínimo de aviso?"""
        return self.cantidad_stock <= self.reorder

    def descontar_stock(self, cantidad):
        if self.cantidad_stock < cantidad:
            raise ValueError(f"No hay suficiente stock para la pieza {self.nombre}")
        self.cantidad_stock -= cantidad
        self.save()

    def reponer_stock(self, cantidad):
        self.cantidad_stock += cantidad
        self.save()


