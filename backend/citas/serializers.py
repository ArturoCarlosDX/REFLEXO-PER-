from rest_framework import serializers
from .models import Cita

# Serializer para el modelo Cita
class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'
        # Puedes personalizar los campos si lo necesitas
