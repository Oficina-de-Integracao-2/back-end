from django.urls import path
from . import views

urlpatterns = [
    path("professor/", views.ProfessorView.as_view())
]
