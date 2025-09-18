
# Vistas para la API REST de citas
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Cita
from .serializers import CitaSerializer

# ViewSet para listar y crear citas

from django.conf import settings
import requests

class CitaViewSet(viewsets.ModelViewSet):
	queryset = Cita.objects.all()
	serializer_class = CitaSerializer

	# Sobrescribimos el método create para reflejar la cita en GHL
	def create(self, request, *args, **kwargs):
		# Crear la cita localmente primero
		response = super().create(request, *args, **kwargs)
		cita = self.get_object()

		# Preparar los datos para GHL
		# Usamos el calendarId real proporcionado por el usuario
		ghl_data = {
			"calendarId": "slBY315jsh4tIJLGWcNx",  # ID real del calendario GHL
			"contact": {
				"name": cita.nombre,
			},
			"date": str(cita.fecha),
			"time": str(cita.hora),
			"description": cita.descripcion,
		}

		# Llamar al endpoint de GHL para reflejar la cita
		ghl_url = "https://api.gohighlevel.com/v1/calendars/events/appointments"
		headers = {
			"Authorization": f"Bearer {settings.GHL_API_TOKEN}",
			"Content-Type": "application/json"
		}
		try:
			r = requests.post(ghl_url, json=ghl_data, headers=headers)
			if r.status_code == 200:
				# Marcar la cita como reflejada en GHL
				cita.creada_en_ghl = True
				cita.save()
		except Exception as e:
			# Puedes loguear el error aquí
			pass
		return response
