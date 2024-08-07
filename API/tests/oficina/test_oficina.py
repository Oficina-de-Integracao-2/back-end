import pytest
from oficina.models import Oficina
from professor.models import Professor
from oficina.serializers import OficinaSerializer
from rest_framework.test import APIRequestFactory
from oficina.permissions import IsAdminOrProfessorOwner
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


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
def test_oficina_model():
    professor = Professor.objects.create_user(
        username='prof_example',
        email='prof@example.com',
        password='password123',
        first_name='Prof',
        last_name='Example',
        cpf='12345678901'
    )
    oficina = Oficina.objects.create(
        title="Test Title",
        description="Test Description",
        workload=10.5,
        city_of_realization="Test City",
        date_of_realization="2024-08-01",
        time_of_realization="10:00:00",
        realized=False,
        professor=professor
    )

    assert oficina.title == "Test Title"
    assert oficina.description == "Test Description"
    assert oficina.workload == 10.5
    assert oficina.city_of_realization == "Test City"
    assert str(oficina.date_of_realization) == "2024-08-01"
    assert str(oficina.time_of_realization) == "10:00:00"
    assert not oficina.realized
    assert oficina.professor == professor


@pytest.mark.django_db
def test_oficina_serializer():
    professor = Professor.objects.create_user(
        username='prof_example',
        email='prof@example.com',
        password='password123',
        first_name='Prof',
        last_name='Example',
        cpf='12345678901'
    )
    oficina = Oficina.objects.create(
        title="Test Title",
        description="Test Description",
        workload=10.5,
        city_of_realization="Test City",
        date_of_realization="2024-08-01",
        time_of_realization="10:00:00",
        realized=False,
        professor=professor
    )
    serializer = OficinaSerializer(oficina)
    data = serializer.data

    assert data["title"] == "Test Title"
    assert data["description"] == "Test Description"
    assert data["workload"] == "10.50"
    assert data["city_of_realization"] == "Test City"
    assert data["date_of_realization"] == "2024-08-01"
    assert data["time_of_realization"] == "10:00:00"
    assert data["realized"] == False
    assert data["professor"]["username"] == "prof_example"


@pytest.mark.django_db
def test_is_admin_or_professor_owner():
    factory = APIRequestFactory()
    user = Professor.objects.create_user(
        username='user_example',
        email='user@example.com',
        password='password123',
        first_name='User',
        last_name='Example',
        cpf='12345678902'
    )
    admin = Professor.objects.create_superuser(
        username='admin_example',
        email='admin@example.com',
        password='adminpassword123',
        first_name='Admin',
        last_name='Example',
        cpf='12345678903'
    )
    another_user = Professor.objects.create_user(
        username='another_user',
        email='another_user@example.com',
        password='password456',
        first_name='Another',
        last_name='User',
        cpf='12345678904'
    )
    oficina = Oficina.objects.create(
        title="Test Title",
        description="Test Description",
        workload=10.5,
        city_of_realization="Test City",
        date_of_realization="2024-08-01",
        time_of_realization="10:00:00",
        realized=False,
        professor=user
    )

    request_user = factory.get('/')
    request_user.user = user

    request_admin = factory.get('/')
    request_admin.user = admin

    request_another_user = factory.get('/')
    request_another_user.user = another_user

    permission = IsAdminOrProfessorOwner()

    assert permission.has_object_permission(request_user, None, oficina) == True, "Proprietário deve ter acesso"
    assert permission.has_object_permission(request_admin, None, oficina) == True, "Administrador deve ter acesso"
    assert permission.has_object_permission(request_another_user, None, oficina) == False, "Outro usuário não deve ter acesso"


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
        'description': 'Aprenda Django com profundidade.',
        'workload': 5.0,
        'city_of_realization': 'New City',
        'date_of_realization': '2024-09-01',
        'time_of_realization': '12:00:00',
        'realized': False,
    }, format='json')
    assert response.status_code == 201, "Usuário autenticado deve poder criar uma oficina."
    assert 'professor' in response.data, "Resposta deve incluir informações do professor."
    assert 'id' in response.data['professor'], "Informações do professor devem incluir um ID."
    assert response.data['professor']['id'] == professor.id, \
           "O professor criador deve ser registrado corretamente na oficina criada."


@pytest.mark.django_db
def test_create_oficina_invalid_data(authenticated_client):
    url = reverse('oficina-list')
    response = authenticated_client.post(url, {}, format='json')
    assert response.status_code == 400, "Deve falhar se os dados obrigatórios não forem fornecidos."


@pytest.mark.django_db
def test_create_oficina_unauthenticated(api_client):
    url = reverse('oficina-list')
    response = api_client.post(url, {
        'title': 'Oficina sem Autenticação',
        'description': 'Deve falhar.',
        'workload': 5.0,
        'city_of_realization': 'New City',
        'date_of_realization': '2024-09-01',
        'time_of_realization': '12:00:00',
        'realized': False,
    }, format='json')
    assert response.status_code == 401, "Usuário não autenticado não deve poder criar uma oficina."


@pytest.mark.django_db
def test_list_oficinas_unauthenticated(api_client):
    url = reverse('oficina-list')
    response = api_client.get(url)
    assert response.status_code == 401, "Usuário não autenticado não deve poder listar oficinas."


@pytest.mark.django_db
def test_update_oficina_authenticated(authenticated_client, professor):
    oficina = Oficina.objects.create(
        title="Oficina Original",
        description="Descrição Original",
        workload=10.5,
        city_of_realization="Cidade Original",
        date_of_realization="2024-08-01",
        time_of_realization="10:00:00",
        realized=False,
        professor=professor
    )
    url = reverse('oficina-detail', args=[oficina.id])
    response = authenticated_client.put(url, {
        'title': 'Oficina Atualizada',
        'description': 'Descrição Atualizada',
        'workload': 8.0,
        'city_of_realization': 'Cidade Atualizada',
        'date_of_realization': '2024-09-01',
        'time_of_realization': '11:00:00',
        'realized': True,
    }, format='json')
    assert response.status_code == 200, "Usuário autenticado deve poder atualizar uma oficina."
    oficina.refresh_from_db()
    assert oficina.title == 'Oficina Atualizada'
    assert oficina.description == 'Descrição Atualizada'
    assert oficina.workload == 8.0
    assert oficina.city_of_realization == 'Cidade Atualizada'
    assert str(oficina.date_of_realization) == '2024-09-01'
    assert str(oficina.time_of_realization) == '11:00:00'
    assert oficina.realized == True


@pytest.mark.django_db
def test_update_oficina_invalid_data(authenticated_client, professor):
    oficina = Oficina.objects.create(
        title="Oficina Original",
        description="Descrição Original",
        workload=10.5,
        city_of_realization="Cidade Original",
        date_of_realization="2024-08-01",
        time_of_realization="10:00:00",
        realized=False,
        professor=professor
    )
    url = reverse('oficina-detail', args=[oficina.id])
    response = authenticated_client.put(url, {}, format='json')
    assert response.status_code == 400, "Deve falhar se os dados obrigatórios não forem fornecidos."


@pytest.mark.django_db
def test_update_oficina_unauthenticated(api_client, professor):
    oficina = Oficina.objects.create(
        title="Oficina Original",
        description="Descrição Original",
        workload=10.5,
        city_of_realization="Cidade Original",
        date_of_realization="2024-08-01",
        time_of_realization="10:00:00",
        realized=False,
        professor=professor
    )
    url = reverse('oficina-detail', args=[oficina.id])
    response = api_client.put(url, {
        'title': 'Oficina Atualizada',
        'description': 'Descrição Atualizada',
        'workload': 8.0,
        'city_of_realization': 'Cidade Atualizada',
        'date_of_realization': '2024-09-01',
        'time_of_realization': '11:00:00',
        'realized': True,
    }, format='json')
    assert response.status_code == 401, "Usuário não autenticado não deve poder atualizar uma oficina."
