from django.contrib import admin
from .models import Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'creado', 'actualizado')
    search_fields = ('codigo', 'nombre', 'descripcion')
    list_filter = ('creado', 'actualizado')