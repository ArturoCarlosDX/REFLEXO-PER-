from rest_framework import serializers
from .models import Cita

# Serializer para el modelo Cita
class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'
        # Aquí puedes dejar todos los campos o especificar solo los que quieras usar
        # Ejemplo: fields = ['calendar_id', 'contact_id', 'title', 'startTime', 'endTime', 'status']

# Serializer para los calendarios (no está ligado a un modelo Django, por eso usamos Serializer)
class CalendarSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    # Mapeamos el valor de isActive de la API externa al campo status del serializer
    status = serializers.BooleanField(source="isActive")
