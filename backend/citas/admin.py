
from django.contrib import admin
from .models import Cita

# Registrar el modelo Cita para que sea visible y editable en el panel de administración
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
	list_display = ("nombre", "fecha", "hora", "creada_en_ghl")
	search_fields = ("nombre", "descripcion")
