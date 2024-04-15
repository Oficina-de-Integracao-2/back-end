from django.urls import path
from . import views


urlpatterns = [
    path("oficina/", views.OficinaView.as_view(), name='oficina-list')
]
