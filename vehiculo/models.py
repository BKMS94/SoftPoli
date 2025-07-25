from django.db import models
from django.urls import reverse

# Define los choices como una lista de tuplas (valor_db, valor_display)
# Es una buena práctica que el valor de la base de datos sea una clave corta y única.
# Aunque aquí usas el mismo string, es válido.
TIPOS_VEHICULO_CHOICES = [
    ('Sedan', 'Sedan'),
    ('Pick-up', 'Pick-up'),
    ('Motocicleta', 'Motocicleta'),
    ('Blindado', 'Blindado'),
    ('Porta tropas', 'Porta tropas'),
    ('Vehículos de rescate', 'Vehículos de rescate'),
    ('Especiales', 'Especiales')
]

ESTADOS_VEHICULO_CHOICES = [
    ('Activo', 'Activo'),
    ('Inoperativo', 'Inoperativo'), # Corregido: 'Pick-up' a 'Inoperativo'
    ('Mantenimiento', 'Mantenimiento'),
]

TIPO_COMBUSTIBLE_CHOICES =[
    ('Gasolina', 'Gasolina'),
    ('Diésel', 'Diésel'), 
    ('GLP', 'GLP'), 
    ('GNV', 'GNV'), 
]

class Vehiculo(models.Model):
    placa = models.CharField(
        max_length=6,
        unique=True,
        verbose_name="Placa"
    )
    vin = models.CharField(
        max_length= 25,

        verbose_name= 'VIN'
    )
    marca = models.CharField(
        max_length=50,
        verbose_name="Marca"
    )
    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo"
    )
    anio = models.PositiveIntegerField(
        verbose_name="Año"
    )
    tipo = models.CharField(
        max_length=30, 
        choices=TIPOS_VEHICULO_CHOICES,
        default='Sedan',
        verbose_name='Tipo'
    )
    kilometraje = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Kilometraje"
    )
    estado = models.CharField(
        max_length=30, 
        choices=ESTADOS_VEHICULO_CHOICES,
        default='Activo', 
        verbose_name='Estado'
    )
    fecha_adquisicion = models.DateTimeField(
        blank=True,
        null= True,
        verbose_name= 'Fecha de adquisición'
    )
    tipo_combustible = models.CharField(
        max_length=20, 
        choices=TIPO_COMBUSTIBLE_CHOICES, 
        default='Gasolina', 
        verbose_name="Tipo de Combustible")

    created = models.DateTimeField(
        auto_now_add=True,
        editable=True
    )

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['created'] 
        
    def __str__(self):
        return self.placa

    def get_detalle_url(self):
        return reverse('vehiculo_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('vehiculo_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('vehiculo_borrar', args=[self.id])
