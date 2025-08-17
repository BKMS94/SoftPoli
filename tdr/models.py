from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower

from vehiculo.models import Vehiculo
from pieza.models import Pieza


class DescripcionServicio(models.Model):
    """
    Modelo para almacenar descripciones de servicios únicas y predefinidas,
    actuando como un catálogo.
    """
    descripcion_servicio = models.TextField(
        unique=True,
        verbose_name="Descripción del Servicio"
    )

    class Meta:
        verbose_name = "Descripción de Servicio (Catálogo)"
        verbose_name_plural = "Descripciones de Servicio (Catálogo)"
        ordering = ['id']
        # Para unicidad case-insensitive en PostgreSQL (si se usa):
        # constraints = [UniqueConstraint(Lower('descripcion_servicio'), name='uniq_desc_servicio_ci')]

    def __str__(self):
        return self.descripcion_servicio


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

    # Reestablecemos el ManyToManyField si queremos poder acceder a las descripciones
    # directamente desde Requerimiento. Si no, se puede omitir.
    # Si lo mantienes, asegúrate de que 'through' apunte correctamente.
    servicios_propuestos = models.ManyToManyField(
        DescripcionServicio,
        through='RequerimientoDescripcionDetalle',
        related_name='requerimientos_asociados_servicio',
        verbose_name="Servicios Propuestos en TDR"
    )

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
    """
    Modelo intermedio para conectar un Requerimiento con las descripciones de servicio.
    Ahora, 'detalle' es un ForeignKey al modelo DescripcionServicio.
    """
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        related_name='detalles_servicio',
        verbose_name="Requerimiento Asociado"
    )
    # ¡CORREGIDO!: 'detalle' es un ForeignKey a DescripcionServicio
    detalle = models.ForeignKey(
        DescripcionServicio,
        on_delete=models.SET_NULL, # Permite que el detalle sea NULL si la DescripcionServicio se borra
        null=True, blank=True, # Puede ser nulo en DB y formularios
        related_name='en_requerimientos_detalle', # Nombre relacionado más específico
        verbose_name="Descripción del Servicio Propuesto"
    )

    class Meta:
        verbose_name = "Detalle de Servicio del Requerimiento"
        verbose_name_plural = "Detalles de Servicios del Requerimiento"
        ordering = ['id']
        constraints = [
            # ¡NUEVO!: Restricción de unicidad para la combinación de requerimiento y detalle
            # Asegura que una descripción de servicio específica solo aparezca una vez por requerimiento.
            UniqueConstraint(
                fields=['requerimiento', 'detalle'],
                name='uniq_req_detalle'
            )
        ]

    def __str__(self):
        # Acceso seguro a la descripción del detalle
        desc_text = self.detalle.descripcion_servicio if self.detalle else "N/A (Descripción eliminada)"
        return f"{desc_text} para Requerimiento {self.requerimiento.id}"


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
