# app/models.py
from django.db import models

class Cita(models.Model):
    calendar_id = models.CharField(max_length=100)      # ID del calendario en GHL
    location_id = models.CharField(max_length=100)      # ID de la ubicación
    contact_id = models.CharField(max_length=100)       # ID del contacto
    start_time = models.DateTimeField()                 # Fecha y hora de inicio
    end_time = models.DateTimeField(null=True, blank=True)  # Fecha y hora de fin, opcional
    title = models.CharField(max_length=255, default="Cita sin título")  # Título opcional
    description = models.TextField(blank=True, default="")  # Descripción opcional
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"{self.title} - {self.start_time}"
