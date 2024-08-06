from .serializers import OficinaSerializer
from rest_framework import generics
from .models import Oficina
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from oficina.permissions import IsAdminOrProfessorOwner


class OficinaView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Oficina.objects.all()
    serializer_class = OficinaSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(professor=self.request.user)


class OficinaDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrProfessorOwner]

    queryset = Oficina.objects.all()
    serializer_class = OficinaSerializer
