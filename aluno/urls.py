from django.urls import path
from . import views

urlpatterns = [
    path("aluno/", views.AlunoView.as_view(), name='aluno-list'),
    path("aluno/<int:pk>/", views.AlunoDetailView.as_view(), name='aluno-detail')
]
