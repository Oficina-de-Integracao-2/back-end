from django.urls import path
from .views import PresencaListCreate, PresencaListByOficina

urlpatterns = [
    path('presenca/', PresencaListCreate.as_view(), name='presenca-list-create'),
    path('presenca/oficina/<int:oficina_id>/', PresencaListByOficina.as_view(), name='presenca-list-by-oficina'),

]
