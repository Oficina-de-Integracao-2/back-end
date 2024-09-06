from django.urls import path
from .views import PresencaListCreate, PresencaListByOficina, UnmarkPresence

urlpatterns = [
    path('presenca/', PresencaListCreate.as_view(), name='presenca-list-create'),
    path('presenca/oficina/<int:oficina_id>/', PresencaListByOficina.as_view(), name='presenca-list-by-oficina'),
    path('presenca/unmark/<int:student_id>/<int:workshop_id>/', UnmarkPresence.as_view(), name='unmark-presenca'),
]
