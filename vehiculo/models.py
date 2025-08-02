from django.db import models
from django.urls import reverse

# Define los choices como una lista de tuplas (valor_db, valor_display)
# Es una buena práctica que el valor de la base de datos sea una clave corta y única.
# Aunque aquí usas el mismo string, es válido.
TIPOS_VEHICULO_CHOICES = [
    ('AMBULANCIA', 'AMBULANCIA'),
    ('AUTOMOVIL', 'AUTOMOVIL'),
    ('AUTOMOVIL SEDAN', 'AUTOMOVIL SEDAN'),
    ('CAMION BARANDA', 'CAMION BARANDA'),
    ('CAMIONETA  FUNERARIO', 'CAMIONETA  FUNERARIO'),
    ('CAMIONETA  PANEL', 'CAMIONETA  PANEL'),
    ('CAMIONETA  PICK UP', 'CAMIONETA  PICK UP'),
    ('CAMIONETA  SUV', 'CAMIONETA  SUV'),
    ('MINIBUS', 'MINIBUS'),
    ('MICROBUS', 'MICROBUS'),
    ('MOTO ACUATICA', 'MOTO ACUATICA'),
    ('MOTOCICLETA', 'MOTOCICLETA'),
    ('MOTOR FUERA DE BORDA ', 'MOTOR FUERA DE BORDA '),
    ('OMNIBUS', 'OMNIBUS'),
    ('PORTATROPA', 'PORTATROPA'),
    ('STATION WAGON', 'STATION WAGON'),
    ('TRIMOTO', 'TRIMOTO')
]

ESTADOS_VEHICULO_CHOICES = [
    ('ACTIVO', 'ACTIVO'),
    ('INOPERATIVO', 'INOPERATIVO'), 
    ('MANTENIMIENTO', 'MANTENIMIENTO'),
]

ESTADOS_ODOMETRO_VEHICULO_CHOICES = [
    ('ACTIVO', 'ACTIVO'),
    ('INOPERATIVO', 'INOPERATIVO'), 
]


TIPO_COMBUSTIBLE_CHOICES =[
    ('GASOLINA', 'GASOLINA'),
    ('DIESEL', 'DIESEL'), 
    ('GLP', 'GLP'), 
    ('GNV', 'GNV'), 
]

FUNCION_VEHICULO_CHOICES = [
    ('ADMINISTRATIVO','ADMINISTRATIVO'),
    ('OPERATIVO','OPERATIVO'),
    ('PATRULLAJE','PATRULLAJE'),
    ('ASIG. AL CARGO','ADMASIG. AL CARGO')
]

class Vehiculo(models.Model):
    placa_int = models.CharField(
        max_length=6,
        unique=True,
        verbose_name="Placa Interna"
    )
    placa_rod = models.CharField(
        max_length=6,
        unique=True,
        verbose_name="Placa Rodaje"
    )
    vin = models.CharField(
        max_length= 20,
        unique=True,
        verbose_name= 'N° de serie'
    )
    num_motor = models.CharField(
        max_length= 25,
        verbose_name= 'N° de motor'
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
    kilometraje = models.DecimalField(
        max_digits= 18,
        decimal_places=1,
        blank=False,
        null=False,
        verbose_name="Kilometraje"
    )
    estado_vehi = models.CharField(
        max_length=30, 
        choices=ESTADOS_VEHICULO_CHOICES,
        default='ACTIVO', 
        verbose_name='Estado del vehículo'
    )
    estado_odo = models.CharField(
        max_length=30, 
        choices=ESTADOS_ODOMETRO_VEHICULO_CHOICES,
        default='ACTIVO', 
        verbose_name='Estado del odometro'
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
        verbose_name="Tipo de Combustible"
    )
    funcion = models.CharField(
        max_length=30, 
        choices=FUNCION_VEHICULO_CHOICES,
        default='ACTIVO', 
        verbose_name='Función policial'
    )
    valor = models.DecimalField(
        max_digits= 18,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Valor"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=True
    )

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['created'] 
        
    def __str__(self):
        return self.placa_int

    def get_detalle_url(self):
        return reverse('vehiculo_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('vehiculo_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('vehiculo_borrar', args=[self.id])
