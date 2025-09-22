# citas/views.py
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CalendarSerializer#aqui

# -------------------------------
# 📌 Listar Calendarios (GET)
# -------------------------------
class ListCalendarsView(APIView):
    def get(self, request):
        # -------------------------------
        # 1️⃣ Obtener parámetro obligatorio locationId
        # -------------------------------
        location_id = request.query_params.get("locationId")
        if not location_id:
            return Response(
                {"error": "locationId is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------
        # 2️⃣ Preparar la URL y headers para la API de GHL
        # -------------------------------
        url = f"https://services.leadconnectorhq.com/calendars/?locationId={location_id}"
        headers = {
            "Authorization": f"Bearer {settings.GHL_API_TOKEN}",
            "Version": "2021-07-28",
            "Content-Type": "application/json"
        }

        # -------------------------------
        # 3️⃣ Llamar a la API de GHL
        # -------------------------------
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Lanza excepción si status code != 200
        except requests.exceptions.HTTPError:
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Network error: {str(e)}"}, status=500)

        # -------------------------------
        # 4️⃣ Serializar los datos obtenidos
        # -------------------------------
        data = response.json().get("calendars", [])
        serializer = CalendarSerializer(data, many=True)

        # -------------------------------
        # 5️⃣ Retornar la lista de calendarios al frontend
        # -------------------------------
        return Response(serializer.data, status=200)



# -------------------------------
# 📌 Listar Citas (GET)
# -------------------------------

class ListAppointmentsView(APIView):
    def get(self, request):
        calendar_id = request.query_params.get("calendarId")
        location_id = request.query_params.get("locationId")
        if not calendar_id or not location_id:
            return Response({"error": "calendarId y locationId son requeridos"}, status=400)

        url = f"{settings.GHL_API_BASE}/calendars/events/appointments/"
        headers = {
            "Authorization": f"Bearer {settings.GHL_API_TOKEN}",
            "Version": settings.GHL_VERSION,
        }
        params = {"calendarId": calendar_id, "locationId": location_id}

        r = requests.get(url, headers=headers, params=params)
        return Response(r.json(), status=r.status_code)




from .models import Cita

# -------------------------------
# 📌 Crear Cita (POST)
# -------------------------------
class CreateAppointmentView(APIView):
    def post(self, request):
        try:
            data = request.data

            # -------------------------------
            # 1️⃣ Validar campos obligatorios
            # -------------------------------
            required_fields = ["calendarId", "locationId", "contactId", "startTime"]
            missing_fields = [f for f in required_fields if f not in data]
            if missing_fields:
                return Response(
                    {"error": f"Faltan campos obligatorios: {', '.join(missing_fields)}"},
                    status=400
                )

            # -------------------------------
            # 2️⃣ Preparar payload para GHL
            # -------------------------------
            payload = {
                "calendarId": data["calendarId"],                # obligatorio
                "locationId": data["locationId"],                # obligatorio
                "contactId": data["contactId"],                  # obligatorio
                "startTime": data["startTime"],                  # obligatorio
                "endTime": data.get("endTime"),                  # opcional
                "title": data.get("title", "Cita sin título"),   # opcional
                "description": data.get("description", ""),      # opcional
            }

            # -------------------------------
            # 3️⃣ Guardar localmente en la base de datos
            # -------------------------------
            Cita.objects.create(
                calendar_id=payload["calendarId"],
                location_id=payload["locationId"],
                contact_id=payload["contactId"],
                start_time=payload["startTime"],
                end_time=payload.get("endTime"),
                title=payload.get("title"),
                description=payload.get("description"),
            )

            # -------------------------------
            # 4️⃣ Enviar la cita a GHL
            # -------------------------------
            url = f"{settings.GHL_API_BASE}/calendars/events/appointments/"
            headers = {
                "Authorization": f"Bearer {settings.GHL_API_TOKEN}",
                "Version": "2021-04-15",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=payload)

            # -------------------------------
            # 5️⃣ Retornar la respuesta de GHL
            # -------------------------------
            try:
                return Response(response.json(), status=response.status_code)
            except Exception:
                return Response({
                    "error": "Respuesta no JSON",
                    "status": response.status_code,
                    "body": response.text
                }, status=response.status_code)

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            return Response({"error": str(e), "traceback": tb}, status=500)
