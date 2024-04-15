import pytest
from django.contrib.auth import get_user_model
from oficina.models import Oficina


Professor = get_user_model()


@pytest.mark.django_db
def test_create_professor_and_oficina():
    """ Testa a criação de uma instância de 'Professor' e sua associação com uma instância de 'Oficina'. """
    professor = Professor.objects.create_user(
        username='professor1',
        first_name='Ana',
        last_name='Silva',
        email='anasilva@example.com',
        cpf='12345678901',
        password='securepassword123'
    )

    oficina = Oficina.objects.create(
        title="Oficina de Testes com Pytest",
        description="Aprenda a criar testes eficientes com Pytest no Django.",
        professor=professor
    )

    assert professor.username == 'professor1', "O username do professor deveria ser 'professor1'."
    assert professor.first_name == 'Ana', "O first name do professor deveria ser 'Ana'."
    assert professor.last_name == 'Silva', "O last name do professor deveria ser 'Silva'."
    assert professor.email == 'anasilva@example.com', "O email do professor deveria ser 'anasilva@example.com'."
    assert professor.cpf == '12345678901', "O CPF do professor deveria ter 11 dígitos."
    assert not professor.is_superuser, "O professor não deveria ser um superusuário."

    assert oficina.professor == professor, "A oficina deveria estar associada ao professor criado."
    assert oficina.title == "Oficina de Testes com Pytest", "O título da oficina deveria ser 'Oficina de Testes com Pytest'."
    assert oficina.description == "Aprenda a criar testes eficientes com Pytest no Django.", "A descrição da oficina deveria cobrir o tema de testes com Pytest."
