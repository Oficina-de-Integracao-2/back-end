import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from professor.models import Professor
from aluno.models import Aluno
from oficina.models import Oficina
from presenca.models import Presenca


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def professor(db):
    return Professor.objects.create_user(
        username="professor1",
        cpf="12345678901",
        first_name="Test",
        last_name="Professor",
        email="professor1@example.com",
        password="password123"
    )


@pytest.fixture
def authenticated_client(api_client, professor):
    api_client.force_authenticate(user=professor)
    return api_client


@pytest.fixture
def aluno(authenticated_client):
    return Aluno.objects.create(
        nome="Aluno Teste",
        cpf="12345678902",
        email="aluno@example.com"
    )


@pytest.fixture
def oficina(professor):
    return Oficina.objects.create(
        title="Oficina Teste",
        description="Descrição da oficina",
        workload=10.0,
        city_of_realization="Cidade Teste",
        date_of_realization="2024-08-14",
        time_of_realization="14:00:00",
        realized=False,
        professor=professor
    )


@pytest.mark.django_db
def test_create_presenca(api_client, aluno, oficina):
    data = {
        "aluno": aluno.id,
        "oficina": oficina.id,
        "presente": True
    }
    response = api_client.post(reverse('presenca-list-create'), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Presenca.objects.count() == 1


@pytest.mark.django_db
def test_list_presenca_by_oficina(api_client, aluno, oficina):
    Presenca.objects.create(aluno=aluno, oficina=oficina, presente=True)

    url = reverse('presenca-list-by-oficina', args=[oficina.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == aluno.id


@pytest.mark.django_db
def test_create_presenca_without_required_fields(authenticated_client, aluno):
    data = {
        "aluno": aluno.id,
        "presente": True
    }
    response = authenticated_client.post(reverse('presenca-list-create'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "oficina" in response.data


@pytest.mark.django_db
def test_create_presenca_with_invalid_aluno(authenticated_client, oficina):
    data = {
        "aluno": 999,
        "oficina": oficina.id,
        "presente": True
    }
    response = authenticated_client.post(reverse('presenca-list-create'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "aluno" in response.data


@pytest.mark.django_db
def test_create_presenca_with_invalid_oficina(authenticated_client, aluno):
    data = {
        "aluno": aluno.id,
        "oficina": 999,
        "presente": True
    }
    response = authenticated_client.post(reverse('presenca-list-create'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "oficina" in response.data


@pytest.mark.django_db
def test_update_presenca(authenticated_client, aluno, oficina):
    presenca = Presenca.objects.create(aluno=aluno, oficina=oficina, presente=False)
    
    data = {
        "aluno": aluno.id,
        "oficina": oficina.id,
        "presente": True
    }
    response = authenticated_client.post(reverse('presenca-list-create'), data)
    
    assert response.status_code == status.HTTP_200_OK
    presenca.refresh_from_db()
    assert presenca.presente is True
    assert Presenca.objects.count() == 1


@pytest.mark.django_db
def test_presenca_unique_constraint(authenticated_client, aluno, oficina):

    Presenca.objects.create(aluno=aluno, oficina=oficina, presente=True)

    data = {
        "aluno": aluno.id,
        "oficina": oficina.id,
        "presente": True
    }
    response = authenticated_client.post(reverse('presenca-list-create'), data)

    assert response.status_code == status.HTTP_200_OK
    assert Presenca.objects.count() == 1


@pytest.mark.django_db
def test_unmark_presenca(authenticated_client, aluno, oficina):

    presenca = Presenca.objects.create(aluno=aluno, oficina=oficina, presente=True)

    url = reverse('unmark-presenca', args=[aluno.id, oficina.id])
    response = authenticated_client.post(url)

    assert response.status_code == status.HTTP_200_OK
    presenca.refresh_from_db()
    assert presenca.presente is False


@pytest.mark.django_db
def test_generate_certificate_without_presence(authenticated_client, aluno, oficina):

    Presenca.objects.create(aluno=aluno, oficina=oficina, presente=False)

    url = reverse('generate-certificate', args=[aluno.id, oficina.id])
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content.decode() == "Certificado não disponível. Presença não registrada."