import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from django.urls import reverse
from professor.serializers import ProfessorSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


@pytest.mark.django_db
def test_create_professor_valid():
    """Teste a criação de um professor com dados válidos."""
    data = {
        'username': 'professor1',
        'first_name': 'Ana',
        'last_name': 'Silva',
        'email': 'anasilva@example.com',
        'cpf': '12345678901',
        'password': 'securepassword123'
    }
    serializer = ProfessorSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    professor = serializer.save()
    assert professor.username == 'professor1'
    assert professor.first_name == 'Ana'
    assert professor.email == 'anasilva@example.com'
    assert professor.cpf == '12345678901'
    assert not professor.is_superuser


@pytest.mark.django_db
def test_professor_unique_email():
    """Testa a unicidade do email."""
    User.objects.create_user(
        username='professor3',
        first_name='Mike',
        last_name='Doe',
        email='mikedoe@example.com',
        cpf='12345678902',
        password='securepassword123'
    )
    data = {
        'username': 'professor4',
        'first_name': 'Michael',
        'last_name': 'Doe',
        'email': 'mikedoe@example.com',
        'cpf': '98765432109',
        'password': 'securepassword321'
    }
    serializer = ProfessorSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_professor_unique_cpf():
    """Testa a unicidade do cpf."""
    User.objects.create_user(
        username='professor5',
        first_name='Laura',
        last_name='Doe',
        email='lauradoe@example.com',
        cpf='11122233344',
        password='password12345'
    )
    data = {
        'username': 'professor6',
        'first_name': 'Linda',
        'last_name': 'Doe',
        'email': 'lindadoe@example.com',
        'cpf': '11122233344',
        'password': 'password54321'
    }
    serializer = ProfessorSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_cpf_validation():
    """Testa se o CPF está sendo validado corretamente."""
    invalid_cpfs = ['123456789', '123456789012', 'abcdefg1234']
    for cpf in invalid_cpfs:
        data = {
            'username': f'invalidcpf_prof_{cpf}',
            'first_name': 'Invalid',
            'last_name': 'CPF',
            'email': f'invalidcpf_{cpf}@example.com',
            'cpf': cpf,
            'password': 'password123'
        }
        serializer = ProfessorSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_professor_missing_data():
    """Testa a criação de um professor com dados faltantes."""
    incomplete_data = [
        {'username': 'incomplete_prof', 'first_name': 'Incomplete', 'email': 'incompleteprof@example.com', 'cpf': '12345678901', 'password': 'password123'},
        {'username': 'incomplete_prof2', 'first_name': 'Incomplete', 'last_name': 'Professor', 'cpf': '12345678901', 'password': 'password123'}
    ]
    for data in incomplete_data:
        serializer = ProfessorSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_professor_invalid_email():
    """Testa a criação de um professor com email inválido."""
    data = {
        'username': 'invalidemail_prof',
        'first_name': 'Invalid',
        'last_name': 'Email',
        'email': 'invalid-email',
        'cpf': '12345678901',
        'password': 'password123'
    }
    serializer = ProfessorSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_professor_empty_fields():
    """Testa a criação de um professor com campos obrigatórios vazios."""
    incomplete_data = [
        {'username': '', 'first_name': 'Empty', 'last_name': 'Field', 'email': 'emptyfield@example.com', 'cpf': '12345678901', 'password': 'password123'},
        {'username': 'emptyfield_prof', 'first_name': '', 'last_name': 'Field', 'email': 'emptyfield@example.com', 'cpf': '12345678901', 'password': 'password123'}
    ]
    for data in incomplete_data:
        serializer = ProfessorSerializer(data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_professor_missing_password():
    """Testa a criação de um professor sem senha."""
    data = {
        'username': 'missingpass_prof',
        'first_name': 'Missing',
        'last_name': 'Password',
        'email': 'missingpass@example.com',
        'cpf': '12345678901',
        'password': ''
    }
    serializer = ProfessorSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_professor_duplicate_username():
    """Testa a criação de um professor com username duplicado."""
    User.objects.create_user(
        username='duplicateuser_prof',
        first_name='Duplicate',
        last_name='User',
        email='duplicateuser1@example.com',
        cpf='12345678901',
        password='password123'
    )
    data = {
        'username': 'duplicateuser_prof',
        'first_name': 'Duplicate',
        'last_name': 'User',
        'email': 'duplicateuser2@example.com',
        'cpf': '12345678902',
        'password': 'password123'
    }
    serializer = ProfessorSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_professor_invalid_first_name():
    """Testa a criação de um professor com first_name inválido."""
    data = {
        'username': 'invalidfirst_prof',
        'first_name': 1234,
        'last_name': 'Valid',
        'email': 'invalidfirst@example.com',
        'cpf': '12345678901',
        'password': 'password123'
    }
    serializer = ProfessorSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_create_professor_invalid_last_name():
    """Testa a criação de um professor com last_name inválido."""
    data = {
        'username': 'invalidlast_prof',
        'first_name': 'Valid',
        'last_name': 1234,
        'email': 'invalidlast@example.com',
        'cpf': '12345678901',
        'password': 'password123'
    }
    serializer = ProfessorSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_jwt_authentication():
    """Testa a autenticação JWT."""
    client = APIClient()
    User.objects.create_user(
        username='auth_professor',
        first_name='Auth',
        last_name='Professor',
        email='authprof@example.com',
        cpf='12345678901',
        password='password123'
    )
    response = client.post(reverse('token_obtain_pair'), {'username': 'auth_professor', 'password': 'password123'})
    assert response.status_code == 200
    tokens = response.json()
    assert 'access' in tokens
    assert 'refresh' in tokens


@pytest.mark.django_db
def test_permissions_is_admin_or_professor_owner():
    """Testa a permissão personalizada IsAdminOrProfessorOwner."""
    client = APIClient()
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        cpf='99999999999',
        password='adminpass'
    )
    professor = User.objects.create_user(
        username='owner_professor',
        first_name='Owner',
        last_name='Professor',
        email='ownerprof@example.com',
        cpf='12345678901',
        password='password123'
    )
    other_professor = User.objects.create_user(
        username='other_professor',
        first_name='Other',
        last_name='Professor',
        email='otherprof@example.com',
        cpf='11111111111',
        password='password123'
    )

    client.force_authenticate(user=other_professor)
    response = client.get(reverse('professor-detail', args=[professor.id]))
    assert response.status_code == 403

    client.force_authenticate(user=admin)
    response = client.get(reverse('professor-detail', args=[professor.id]))
    assert response.status_code == 200

    client.force_authenticate(user=professor)
    response = client.get(reverse('professor-detail', args=[professor.id]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_professor_valid():
    """Testa a atualização dos dados de um professor com dados válidos."""
    professor = User.objects.create_user(
        username='update_prof',
        first_name='Update',
        last_name='Professor',
        email='updateprof@example.com',
        cpf='12345678901',
        password='oldpassword'
    )
    data = {
        'first_name': 'Updated',
        'last_name': 'Professor',
        'email': 'updatedprof@example.com',
        'cpf': '12345678901',
        'password': 'newpassword123'
    }
    serializer = ProfessorSerializer(instance=professor, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_professor = serializer.save()
    assert updated_professor.first_name == 'Updated'
    assert updated_professor.check_password('newpassword123')


@pytest.mark.django_db
def test_update_professor_invalid():
    """Testa a atualização dos dados de um professor com dados inválidos."""
    professor = User.objects.create_user(
        username='update_prof_invalid',
        first_name='Update',
        last_name='Professor',
        email='updateprofinvalid@example.com',
        cpf='12345678901',
        password='oldpassword'
    )
    data = {
        'first_name': 'Invalid123',
        'last_name': 'Professor',
        'email': 'updateprofinvalid@example.com',
        'cpf': '12345678901',
        'password': 'newpassword123'
    }
    serializer = ProfessorSerializer(instance=professor, data=data, partial=True)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_list_professors():
    """Testa a listagem de professores."""
    User.objects.create_user(
        username='professor1',
        first_name='Ana',
        last_name='Silva',
        email='ana.silva@example.com',
        cpf='12345678901',
        password='password123'
    )
    User.objects.create_user(
        username='professor2',
        first_name='Bruno',
        last_name='Costa',
        email='bruno.costa@example.com',
        cpf='12345678902',
        password='password123'
    )
    client = APIClient()
    response = client.get(reverse('professor-list'))
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2


@pytest.mark.django_db
def test_retrieve_professor_detail():
    """Testa a recuperação dos detalhes de um professor específico."""
    professor = User.objects.create_user(
        username='detail_prof',
        first_name='Detail',
        last_name='Professor',
        email='detailprof@example.com',
        cpf='12345678901',
        password='password123'
    )

    client = APIClient()
    tokens = RefreshToken.for_user(professor)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens.access_token}')

    response = client.get(reverse('professor-detail', args=[professor.id]))
    assert response.status_code == 200
    result = response.json()
    assert result['username'] == 'detail_prof'
    assert result['first_name'] == 'Detail'
    assert result['last_name'] == 'Professor'
    assert result['email'] == 'detailprof@example.com'
    assert result['cpf'] == '12345678901'
