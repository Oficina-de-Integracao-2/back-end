import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
Professor = get_user_model()


@pytest.mark.django_db
def test_oficina_view():
    """ Testa a obtenção e criação de oficinas através da OficinaView. """
    client = APIClient()
    professor = Professor.objects.create_user(
        username='professor_test',
        email='professor@test.com',
        password='testpass123',
        first_name="John",
        last_name="Doe",
        cpf='12345678901'
    )
    refresh = RefreshToken.for_user(professor)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    url = reverse('oficina-list')

    response = client.get(url)
    assert response.status_code == 200, "Usuário autenticado deve poder listar oficinas."

    response = client.post(url, {
        'title': 'Nova Oficina de Django',
        'description': 'Aprenda Django com profundidade.'
    })
    assert response.status_code == 201, "Usuário autenticado deve poder criar uma oficina."
    assert response.data['professor']['id'] == professor.id, "O professor criador deve ser registrado corretamente na oficina criada."

    client.credentials()
    response = client.get(url)
    assert response.status_code == 401, "Usuário não autenticado não deve poder listar oficinas."

    response = client.post(url, {
        'title': 'Oficina sem Autenticação',
        'description': 'Deve falhar.'
    })
    assert response.status_code == 401, "Usuário não autenticado não deve poder criar uma oficina."

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    response = client.post(url, {})
    assert response.status_code == 400, "Deve falhar se os dados obrigatórios não forem fornecidos."
