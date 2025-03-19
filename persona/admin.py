from django.contrib import admin
from .models import  Persona, Tecnico
# Register your models here.

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','grado','telefono']
    search_fields = ['codigo', 'nombre']



@admin.register(Tecnico)
class TecnicoAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','grado','telefono']
    search_fields = ['codigo', 'nombre']