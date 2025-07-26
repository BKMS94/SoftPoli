from django.db import models
from django.urls import reverse


# Create your models here.
class Grado(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False, verbose_name=' Nombre del Grado', unique= True)
    abreviatura = models.CharField(max_length= 10, unique=True, verbose_name= 'Abreviatura', blank= True, null= True)
    orden = models.CharField(default= 0, verbose_name='Orden Jerárquico')

    class Meta:
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre
    
    def get_detalle_url(self):
        return reverse('grado_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('grado_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('grado_borrar', args=[self.id])