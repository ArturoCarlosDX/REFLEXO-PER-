from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    # Mostramos solo los campos que existen en el modelo
    list_display = ("title", "description", "calendar_id", "location_id", "contact_id", "start_time", "end_time")
    search_fields = ("title", "description", "contact_id")
    list_filter = ("calendar_id", "location_id")
    
