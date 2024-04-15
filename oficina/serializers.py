from rest_framework import serializers
from .models import Oficina
from professor.serializers import ProfessorSerializer


class OficinaSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)

    class Meta:
        model = Oficina
        fields = ["id", "title", "description", "professor"]