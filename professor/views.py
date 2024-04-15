from .serializers import ProfessorSerializer
from rest_framework import generics
from .models import Professor


class ProfessorView(generics.ListCreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
