from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower # Importar Lower para unicidad case-insensitive


# ¡ELIMINADO!: El modelo DescripcionServicio ha sido removido completamente.
# No será usado para los servicios del TDR ni se asume su uso en otras apps desde aquí.

from vehiculo.models import Vehiculo
from pieza.models import Pieza


class Requerimiento(models.Model):
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='requerimientos',
        verbose_name="Vehículo del Requerimiento"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación del TDR",
        db_index=True
    )
    informe_tecnico_nro = models.CharField(
        unique=True,
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Nº Informe Técnico"
    )

    # Piezas Propuestas se mantiene igual
    piezas_propuestas = models.ManyToManyField(
        Pieza,
        through='RequerimientoPiezaDetalle',
        related_name='en_requerimientos',
        verbose_name="Piezas Propuestas en TDR"
    )

    class Meta:
        verbose_name = "Requerimiento TDR"
        verbose_name_plural = "Requerimientos TDRs"
        ordering = ['-fecha_creacion']

    def __str__(self):
        fecha = timezone.localtime(self.fecha_creacion).strftime('%d/%m/%Y')
        return f"TDR #{self.id} - Vehículo: {self.vehiculo.placa_int} ({fecha})"

    def get_absolute_url(self):
        return reverse('detalle_requerimiento', args=[self.id])

    def get_editar_url(self):
        return reverse('editar_requerimiento', args=[self.id])

    def get_borrar_url(self):
        return reverse('borrar_requerimiento', args=[self.id])


class RequerimientoDescripcionDetalle(models.Model):
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        related_name='detalles_servicio',
        verbose_name="Requerimiento Asociado"
    )
    descripcion_propuesta = models.TextField(
        verbose_name="Descripción del Servicio Propuesto",
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = "Detalle de Servicio del Requerimiento"
        verbose_name_plural = "Detalles de Servicios del Requerimiento"
        ordering = ['id']
        constraints = [
            UniqueConstraint(
                fields=['requerimiento', 'descripcion_propuesta'],
                name='uniq_req_desc'
            )
        ]

    def __str__(self):
        return f"{self.descripcion_propuesta} para Requerimiento {self.requerimiento.id}"


class RequerimientoPiezaDetalle(models.Model):
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        related_name='detalles_pieza',
        verbose_name="Requerimiento Asociado"
    )
    pieza = models.ForeignKey(
        Pieza,
        on_delete=models.CASCADE,
        related_name='en_requerimientos_piezas',
        verbose_name="Pieza Propuesta"
    )
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad Propuesta")

    class Meta:
        verbose_name = "Detalle de Pieza del Requerimiento"
        verbose_name_plural = "Detalles de Piezas del Requerimiento"
        ordering = ['id']
        constraints = [
            UniqueConstraint(fields=['requerimiento', 'pieza'], name='uniq_req_pieza')
        ]

    def __str__(self):
        return f"{self.cantidad} x {self.pieza.nombre} para TDR {self.requerimiento.id}"
