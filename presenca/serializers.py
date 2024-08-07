from rest_framework import serializers
from .models import Presenca
from aluno.models import Aluno
from oficina.models import Oficina


class PresencaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presenca
        fields = ['id', 'aluno', 'oficina', 'presente']

    aluno = serializers.PrimaryKeyRelatedField(queryset=Aluno.objects.all())
    oficina = serializers.PrimaryKeyRelatedField(queryset=Oficina.objects.all())
