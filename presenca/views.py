from rest_framework import generics
from .models import Presenca
from .serializers import PresencaSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from aluno.serializers import AlunoSerializer


class PresencaListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Presenca.objects.all()
    serializer_class = PresencaSerializer


class PresencaListByOficina(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, oficina_id):
        presencas = Presenca.objects.filter(oficina_id=oficina_id, presente=True)
        alunos_presentes = [presenca.aluno for presenca in presencas]
        serializer = AlunoSerializer(alunos_presentes, many=True)
        return Response(serializer.data)
