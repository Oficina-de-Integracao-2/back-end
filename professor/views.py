from .serializers import ProfessorSerializer
from rest_framework import generics
from .models import Professor
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from professor.permissions import IsAdminOrProfessorOwner


class ProfessorView(generics.ListCreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class ProfessorDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrProfessorOwner]

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
