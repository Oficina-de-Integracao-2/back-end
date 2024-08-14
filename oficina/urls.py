from django.urls import path
from . import views


urlpatterns = [
    path("oficina/", views.OficinaView.as_view(), name='oficina-list'),
    path("oficina/<int:pk>/", views.OficinaDetailView.as_view(), name='oficina-detail'),
    path("oficina/professor/<int:professor_id>/", views.OficinasPorProfessorView.as_view(), name='oficinas-por-professor')
]
