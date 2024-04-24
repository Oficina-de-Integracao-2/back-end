import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from professor.models import Professor
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def professor(db):
    """Cria um professor para ser usado nos testes."""
    user = Professor.objects.create_user(
        username="professor1",
        email="professor1@example.com",
        cpf="12345678901",
        first_name="John",
        last_name="Doe",
        password="verysecure"
    )
    return user


@pytest.mark.django_db
def test_list_professors(client, professor):
    """Verifica se a listagem de professores está correta."""
    url = reverse('professor-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK, "A resposta deve ser 200 OK."
    assert len(response.data) == 1, "Deveria haver exatamente 1 professor listado."
    assert response.data[0]['username'] == 'professor1', "O username do professor listado está incorreto."
    assert response.data[0]['email'] == 'professor1@example.com', "O email do professor listado está incorreto."
    assert response.data[0]['cpf'] == '12345678901', "O CPF do professor listado está incorreto."


@pytest.mark.django_db
def test_create_professor(client, professor):
    """Testa a criação de um novo professor via API."""
    url = reverse('professor-list')
    professor_data = {
        'username': 'professor2',
        'email': 'professor2@example.com',
        'cpf': '98765432109',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'password': 'securepassword123'
    }
    response = client.post(url, professor_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED, "Falha na criação: a resposta deveria ser 201 CREATED."
    assert Professor.objects.count() == 2, "Deveriam existir 2 professores no banco de dados."
    new_professor = Professor.objects.get(username='professor2')
    assert new_professor.email == 'professor2@example.com', "O email do novo professor não corresponde."
    assert new_professor.cpf == '98765432109', "O CPF do novo professor não corresponde."


@pytest.mark.django_db
def test_login_success(client, professor):
    """Verifica se o login com credenciais corretas gera tokens de acesso e refresh."""
    url = reverse('token_obtain_pair')
    login_data = {
        'username': 'professor1',
        'password': 'verysecure'
    }
    response = client.post(url, login_data)
    assert response.status_code == status.HTTP_200_OK, "O status de resposta deveria ser 200 OK ao fazer login."
    assert 'access' in response.data, "Deveria haver um token de acesso na resposta."
    assert 'refresh' in response.data, "Deveria haver um token de refresh na resposta."


@pytest.mark.django_db
def test_refresh_token(client, professor):
    """Testa a renovação do token de acesso usando um token de refresh válido."""
    refresh = RefreshToken.for_user(professor)
    url = reverse('token_refresh')
    refresh_data = {
        'refresh': str(refresh)
    }
    response = client.post(url, refresh_data)
    assert response.status_code == status.HTTP_200_OK, "O status de resposta deveria ser 200 OK ao renovar o token."
    assert 'access' in response.data, "Deveria haver um token de acesso renovado na resposta."


@pytest.mark.django_db
def test_login_failure(client):
    """Verifica se o login com credenciais incorretas é adequadamente negado."""
    url = reverse('token_obtain_pair')
    login_data = {
        'username': 'wrong_user',
        'password': 'wrong_password'
    }
    response = client.post(url, login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, "O status de resposta deveria ser 401 UNAUTHORIZED para credenciais incorretas."


@pytest.mark.django_db
def test_login_failure_with_wrong_password(client, professor):
    """Verifica o login com senha incorreta."""
    url = reverse('token_obtain_pair')
    login_data = {
        'username': 'professor1',
        'password': 'wrongpassword'
    }
    response = client.post(url, login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Deveria retornar 401 UNAUTHORIZED para senha incorreta."


@pytest.mark.django_db
def test_create_professor_with_invalid_data(client):
    """Testa a criação de um professor com dados inválidos."""
    url = reverse('professor-list')
    invalid_professor_data = {
        'username': 'professor3',
        'email': 'invalid-email',
        'cpf': '1234567890',
        'first_name': 'Invalid',
        'last_name': 'Professor',
        'password': 'pass'
    }
    response = client.post(url, invalid_professor_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST, "Deveria retornar 400 BAD REQUEST para dados inválidos."
    assert 'email' in response.data, "Deveria retornar erro para o email inválido."
    assert 'cpf' in response.data, "Deveria retornar erro para o CPF inválido."