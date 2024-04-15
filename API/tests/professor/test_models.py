import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate


User = get_user_model()


@pytest.mark.django_db
def test_create_professor_valid():
    """Teste a criação de um professor com dados válidos."""
    professor = User.objects.create_user(
        username='professor1',
        first_name='Ana',
        last_name='Silva',
        email='anasilva@example.com',
        cpf='12345678901',
        password='securepassword123'
    )
    assert professor.username == 'professor1', "O username do professor deveria ser 'professor1'."
    assert professor.first_name == 'Ana', "O first name do professor deveria ser 'Ana'."
    assert professor.email == 'anasilva@example.com', "O email do professor deveria ser 'anasilva@example.com'."
    assert professor.cpf == '12345678901', "O CPF do professor deveria ter 11 dígitos."
    assert not professor.is_superuser, "O professor não deveria ser um superusuário."


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
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username='professor4',
            first_name='Michael',
            last_name='Doe',
            email='mikedoe@example.com',
            cpf='98765432109',
            password='securepassword321'
        )
    assert "deveria falhar devido ao email duplicado", "A criação de um usuário com email duplicado deveria levantar uma IntegrityError."


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
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username='professor6',
            first_name='Linda',
            last_name='Doe',
            email='lindadoe@example.com',
            cpf='11122233344',
            password='password54321'
        )
    assert "deveria falhar devido ao CPF duplicado", "A criação de um usuário com CPF duplicado deveria levantar uma IntegrityError."


@pytest.mark.django_db
def test_cpf_validation():
    """Testa se o CPF está sendo validado corretamente."""
    with pytest.raises(ValidationError) as excinfo:
        user = User(
            username='professor_invalid_cpf',
            first_name='Invalid',
            last_name='CPF',
            email='invalidcpf@example.com',
            cpf='123456789',
            password='password123'
        )
        user.full_clean()
    assert "CPF deve ter 11 dígitos." in str(excinfo.value), "O CPF com menos de 11 dígitos deveria levantar ValidationError."

    with pytest.raises(ValidationError) as excinfo:
        user2 = User(
            username='professor_invalid_cpf2',
            first_name='Invalid',
            last_name='CPF2',
            email='invalidcpf2@example.com',
            cpf='123456789012',
            password='password123'
        )
        user2.full_clean()
    assert "CPF deve ter 11 dígitos." in str(excinfo.value), "O CPF com mais de 11 dígitos deveria levantar ValidationError."


@pytest.mark.django_db
def test_update_professor():
    """Testa a atualização dos dados de um professor."""

    professor = User.objects.create_user(
        username='update_prof',
        first_name='Update',
        last_name='Professor',
        email='updateprof@example.com',
        cpf='12345678901',
        password='oldpassword'
    )
    professor.first_name = 'Updated'
    professor.save()
    updated_professor = User.objects.get(username='update_prof')
    assert updated_professor.first_name == 'Updated', "A atualização do primeiro nome falhou."


@pytest.mark.django_db
def test_delete_professor():
    """Testa a exclusão de um professor."""

    professor = User.objects.create_user(
        username='delete_prof',
        first_name='Delete',
        last_name='Professor',
        email='deleteprof@example.com',
        cpf='12345678901',
        password='password123'
    )
    professor_id = professor.id
    professor.delete()
    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=professor_id)




