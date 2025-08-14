from django.db import models
from django.urls import reverse
from django.utils import timezone # Para campos de fecha/hora

# Importa los modelos existentes de otras apps
from vehiculo.models import Vehiculo
from pieza.models import Pieza
# Ya NO importamos DescripcionServicio desde 'servicios.models' aquí,
# porque DescripcionServicio estará definido LOCALMENTE en esta app.

# --- Modelos de Requerimientos (TDR) ---

class Requerimiento(models.Model):
    """
    Representa un documento de Términos de Referencia (TDR)
    para el servicio de mantenimiento de un vehículo.
    Este modelo utiliza los campos directamente proporcionados en tu última revisión.
    """
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        verbose_name="Vehículo del Requerimiento"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación del TDR"
    )
    informe_tecnico_nro = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Nº Informe Técnico"
    )
    

    # --- Reestableciendo los ManyToManyField con 'through' models ---
    # Son cruciales para gestionar múltiples servicios y piezas en el TDR
    servicios_propuestos = models.ManyToManyField(
        'DescripcionServicio', # Referencia al modelo DescripcionServicio LOCAL en esta app
        through='RequerimientoDescripcionDetalle',
        related_name='requerimientos_asociados_servicio',
        verbose_name="Servicios Propuestos en TDR"
    )
    piezas_propuestas = models.ManyToManyField(
        Pieza,
        through='RequerimientoPiezaDetalle',
        related_name='requerimientos_asociados_pieza',
        verbose_name="Piezas Propuestas en TDR"
    )


    class Meta:
        verbose_name = "Requerimiento TDR"
        verbose_name_plural = "Requerimientos TDRs"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"TDR #{self.id} - Vehículo: {self.vehiculo.placa_int} ({self.fecha_creacion.strftime('%d/%m/%Y')})"

    def get_absolute_url(self):
        return reverse('detalle_requerimiento', args=[self.id])
    
    def get_editar_url(self):
        return reverse('editar_requerimiento', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('borrar_requerimiento', args=[self.id])


class DescripcionServicio(models.Model):
    """
    Modelo para almacenar descripciones de servicios únicas
    dentro de la aplicación 'requerimientos' (para los TDRs).
    """
    descripcion_servicio = models.TextField(
        unique=True, # ¡CORREGIDO!: Asegura unicidad del texto de la descripción
        verbose_name="Descripción del Servicio Propuesto"
    )

    class Meta:
        # unique_together = ('descripcion_servicio') # ¡ELIMINADO!: No es necesario con unique=True en el campo
        verbose_name = "Descripción de Servicio (TDR)" # Cambiado para mayor claridad
        verbose_name_plural = "Descripciones de Servicio (TDR)" # Cambiado para mayor claridad

    def __str__(self):
        return self.descripcion_servicio # ¡CORREGIDO!: Retorna el campo directamente


class RequerimientoDescripcionDetalle(models.Model):
    """
    Modelo intermedio para conectar un Requerimiento con las Descripciones de Servicio propuestas
    (del modelo DescripcionServicio LOCAL a la app 'requerimientos').
    """
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        verbose_name="Requerimiento Asociado"
    )
    # ¡CORREGIDO!: Apunta al modelo DescripcionServicio LOCAL de esta misma app
    # ¡NUEVO!: Se permite que sea nulo y en blanco para manejar datos inconsistentes o futuras eliminaciones.
    detalle = models.ForeignKey(
        DescripcionServicio, # Usa el modelo DescripcionServicio LOCAL
        on_delete=models.SET_NULL, # Si DescripcionServicio es eliminado, este campo se vuelve NULL
        null=True, # Permite que el campo sea NULL en la base de datos
        blank=True, # Permite que el campo sea BLANK en formularios
        verbose_name="Descripción del Servicio Propuesto"
    )


    class Meta:
        # unique_together = ('requerimiento', 'detalle') # Si detalle puede ser NULL, unique_together puede necesitar un índice parcial
                                                         # Sin embargo, con NULL permitidos, Django no lo considera único si es NULL.
        verbose_name = "Detalle de Servicio del Requerimiento"
        verbose_name_plural = "Detalles de Servicios del Requerimiento"

    def __str__(self):
        # ¡CORREGIDO!: Accede a la descripción a través de la relación 'detalle' de forma segura
        # Esto evitará el error si 'detalle' es NULL
        desc_text = self.detalle.descripcion_servicio if self.detalle else "N/A"
        return f"{desc_text} para Requerimiento {self.requerimiento.id}"


class RequerimientoPiezaDetalle(models.Model):
    """
    Modelo intermedio para conectar un Requerimiento con las Piezas propuestas y sus cantidades.
    """
    requerimiento = models.ForeignKey(
        Requerimiento,
        on_delete=models.CASCADE,
        verbose_name="Requerimiento Asociado"
    )
    pieza = models.ForeignKey(
        Pieza,
        on_delete=models.CASCADE,
        verbose_name="Pieza Propuesta"
    )
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad Propuesta"
    )

    class Meta:
        unique_together = ('requerimiento', 'pieza') # No repetir la misma pieza en el mismo TDR
        verbose_name = "Detalle de Pieza del Requerimiento"
        verbose_name_plural = "Detalles de Piezas del Requerimiento" # ¡CORREGIDO!: verbose_plural -> verbose_name_plural

    def __str__(self):
        return f"{self.cantidad} x {self.pieza.nombre} para TDR {self.requerimiento.id}"
