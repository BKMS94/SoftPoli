from django.db import models
from django.urls import reverse
from grado.models import Grado
# Create your models here.

class Persona(models.Model):
    codigo = models.CharField(unique=True ,max_length=12, blank= False, null= False)
    nombre = models.CharField(max_length=100, blank=False, null= False)
    grado = models.ForeignKey(Grado , on_delete= models.CASCADE)
    telefono = models.CharField (max_length= 12, blank= False, null=False)
    created = models.DateTimeField(editable=None, auto_now=True)

    def __str__(self):
        return self.nombre

    def get_detalle_url(self):
        return reverse('persona_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('persona_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('persona_borrar', args=[self.id])

class Tecnico(models.Model):
    codigo = models.CharField(unique=True ,max_length=12, blank= False, null= False)
    nombre = models.CharField(max_length=100, blank=False, null= False)
    grado = models.ForeignKey(Grado , on_delete= models.CASCADE)
    telefono = models.CharField (max_length= 12, blank= False, null=False)
    created = models.DateTimeField(editable=None, auto_now=True)
    def __str__(self):
        return self.nombre
    
    def get_detalle_url(self):
        return reverse('tecnico_detalle', args=[self.id])
    
    def get_editar_url(self):
        return reverse('tecnico_editar', args=[self.id])
    
    def get_borrar_url(self):
        return reverse('tecnico_borrar', args=[self.id])