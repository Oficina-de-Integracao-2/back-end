import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


Professor = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def professor(db):
    return Professor.objects.create_user(
        username='professor_test',
        email='professor@test.com',
        password='testpass123',
        first_name="John",
        last_name="Doe",
        cpf='12345678901'
    )


@pytest.fixture
def authenticated_client(api_client, professor):
    refresh = RefreshToken.for_user(professor)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.mark.django_db
def test_list_oficinas_authenticated(authenticated_client):
    url = reverse('oficina-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200, "Usuário autenticado deve poder listar oficinas."


@pytest.mark.django_db
def test_create_oficina_authenticated(authenticated_client, professor):
    url = reverse('oficina-list')
    response = authenticated_client.post(url, {
        'title': 'Nova Oficina de Django',
        'description': 'Aprenda Django com profundidade.'
    })
    assert response.status_code == 201, "Usuário autenticado deve poder criar uma oficina."
    assert 'professor' in response.data, "Resposta deve incluir informações do professor."
    assert 'id' in response.data['professor'], "Informações do professor devem incluir um ID."
    assert response.data['professor']['id'] == professor.id, \
           "O professor criador deve ser registrado corretamente na oficina criada."


@pytest.mark.django_db
def test_list_oficinas_unauthenticated(api_client):
    url = reverse('oficina-list')
    response = api_client.get(url)
    assert response.status_code == 401, "Usuário não autenticado não deve poder listar oficinas."


@pytest.mark.django_db
def test_create_oficina_unauthenticated(api_client):
    url = reverse('oficina-list')
    response = api_client.post(url, {
        'title': 'Oficina sem Autenticação',
        'description': 'Deve falhar.'
    })
    assert response.status_code == 401, "Usuário não autenticado não deve poder criar uma oficina."


@pytest.mark.django_db
def test_create_oficina_invalid_data(authenticated_client):
    url = reverse('oficina-list')
    response = authenticated_client.post(url, {})
    assert response.status_code == 400, "Deve falhar se os dados obrigatórios não forem fornecidos."
