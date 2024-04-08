import pytest
from django.core.exceptions import ValidationError
from professor.models import Professor
from django.db import IntegrityError
from django.db import transaction


@pytest.mark.django_db
def test_create_professor():
    professor_data = {
        "name": "Dr. Ana Silva",
        "email": "anasilva@example.com",
        "cpf": "12345678901",
    }

    professor = Professor.objects.create(**professor_data)

    assert Professor.objects.count() == 1, "Deveria haver exatamente um professor no banco de dados."
    assert professor.name == professor_data["name"], "O nome do professor não corresponde ao esperado."
    assert professor.email == professor_data["email"], "O email do professor não corresponde ao esperado."
    assert professor.cpf == professor_data["cpf"], "O CPF do professor não corresponde ao esperado."


@pytest.mark.django_db
def test_cpf_unique():
    Professor.objects.create(name="Prof. Carlos", email="carlos@example.com", cpf="11122233344")

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            professor = Professor(name="Prof. Carlos", email="carlos2@example.com", cpf="11122233344")
            professor.save()


@pytest.mark.django_db
def test_cpf_length():
    with pytest.raises(ValidationError):
        professor = Professor(name="Prof. Joana", email="joana@example.com", cpf="123456789")
        professor.full_clean()
