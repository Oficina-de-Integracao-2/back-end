import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from aluno.models import Aluno
from aluno.serializers import AlunoSerializer
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from professor.models import Professor


@pytest.fixture
def api_client():
    client = APIClient()
    professor = Professor.objects.create_user(
        username="testprofessor",
        password="testpass",
        first_name="Test",
        last_name="Professor",
        email="testprofessor@example.com",
        cpf="12345678901"
    )
    refresh = RefreshToken.for_user(professor)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


@pytest.mark.django_db
def test_invalid_cpf_length():
    with pytest.raises(ValidationError):
        aluno = Aluno(nome="João da Silva", cpf="123456789", email="joao@example.com")
        aluno.full_clean()


@pytest.mark.django_db
def test_create_aluno_invalid_cpf():
    client = APIClient()
    aluno_data = {"nome": "João da Silva", "cpf": "12345678", "email": "joao@example.com"}
    response = client.post(reverse('aluno-list'), data=aluno_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cpf" in response.data


@pytest.mark.django_db
def test_create_aluno_missing_name():
    client = APIClient()
    aluno_data = {"cpf": "12345678901", "email": "joao@example.com"}
    response = client.post(reverse('aluno-list'), data=aluno_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nome" in response.data


@pytest.mark.django_db
def test_create_aluno_duplicate_cpf():
    client = APIClient()
    Aluno.objects.create(nome="João da Silva", cpf="12345678901", email="joao@example.com")
    aluno_data = {"nome": "Maria Souza", "cpf": "12345678901", "email": "maria@example.com"}
    response = client.post(reverse('aluno-list'), data=aluno_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cpf" in response.data


@pytest.mark.django_db
def test_create_aluno_invalid_email():
    client = APIClient()
    aluno_data = {"nome": "João da Silva", "cpf": "12345678901", "email": "invalid-email"}
    response = client.post(reverse('aluno-list'), data=aluno_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_update_aluno_invalid_cpf(api_client):
    aluno = Aluno.objects.create(nome="João da Silva", cpf="12345678901", email="joao@example.com")
    update_data = {"cpf": "12345678"}
    response = api_client.put(reverse('aluno-detail', args=[aluno.id]), data=update_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "cpf" in response.data


@pytest.mark.django_db
def test_update_aluno_duplicate_email(api_client):
    Aluno.objects.create(nome="Maria Souza", cpf="98765432100", email="maria@example.com")
    aluno = Aluno.objects.create(nome="João da Silva", cpf="12345678901", email="joao@example.com")
    update_data = {"email": "maria@example.com"}
    response = api_client.put(reverse('aluno-detail', args=[aluno.id]), data=update_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_update_aluno_missing_name(api_client):
    aluno = Aluno.objects.create(nome="João da Silva", cpf="12345678901", email="joao@example.com")
    update_data = {"nome": ""}
    response = api_client.put(reverse('aluno-detail', args=[aluno.id]), data=update_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "nome" in response.data


@pytest.mark.django_db
def test_aluno_serializer():
    aluno_data = {"nome": "João da Silva", "cpf": "12345678901", "email": "joao@example.com"}
    serializer = AlunoSerializer(data=aluno_data)
    assert serializer.is_valid()
    aluno = serializer.save()
    assert Aluno.objects.count() == 1
    assert aluno.nome == "João da Silva"


@pytest.mark.django_db
def test_aluno_serializer_invalid_cpf():
    aluno_data = {"nome": "João da Silva", "cpf": "12345678", "email": "joao@example.com"}
    serializer = AlunoSerializer(data=aluno_data)
    assert not serializer.is_valid()
    assert "cpf" in serializer.errors


@pytest.mark.django_db
def test_get_aluno_list():
    client = APIClient()
    response = client.get(reverse('aluno-list'))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_aluno():
    client = APIClient()
    aluno_data = {"nome": "João da Silva", "cpf": "12345678901", "email": "joao@example.com"}
    response = client.post(reverse('aluno-list'), data=aluno_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Aluno.objects.count() == 1


@pytest.mark.django_db
def test_get_aluno_detail(api_client):
    aluno = Aluno.objects.create(nome="João da Silva", cpf="12345678901", email="joao@example.com")
    response = api_client.get(reverse('aluno-detail', args=[aluno.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['nome'] == "João da Silva"


@pytest.mark.django_db
def test_update_aluno(api_client):
    aluno = Aluno.objects.create(nome="João da Silva", cpf="12345678901", email="joao@example.com")
    update_data = {"nome": "João da Silva Junior"}
    response = api_client.patch(reverse('aluno-detail', args=[aluno.id]), data=update_data)
    assert response.status_code == status.HTTP_200_OK
    aluno.refresh_from_db()
    assert aluno.nome == "João da Silva Junior"


@pytest.mark.django_db
def test_delete_aluno(api_client):
    aluno = Aluno.objects.create(nome="João da Silva", cpf="12345678901", email="joao@example.com")
    response = api_client.delete(reverse('aluno-detail', args=[aluno.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Aluno.objects.count() == 0
