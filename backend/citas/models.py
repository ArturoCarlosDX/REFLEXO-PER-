
from django.db import models

# Modelo para almacenar las citas agendadas en ReflexoPeru
class Cita(models.Model):
	nombre = models.CharField(max_length=100, help_text="Nombre del paciente")
	fecha = models.DateField(help_text="Fecha de la cita")
	hora = models.TimeField(help_text="Hora de la cita")
	descripcion = models.TextField(blank=True, help_text="Descripción de la cita")
	creada_en_ghl = models.BooleanField(default=False, help_text="¿La cita fue reflejada en GHL?")

	def __str__(self):
		return f"{self.nombre} - {self.fecha} {self.hora}"
