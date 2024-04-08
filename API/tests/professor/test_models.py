import pytest
from django.core.exceptions import ValidationError
from professor.models import Professor


@pytest.mark.django_db
def test_create_professor():
    professor_data = {
        "name": "Dr. Ana Silva",
        "email": "anasilva@example.com",
        "cpf": "12345678901",
    }

    professor = Professor.objects.create(**professor_data)

    assert Professor.objects.count() == 1

    assert professor.name == professor_data["name"]
    assert professor.email == professor_data["email"]
    assert professor.cpf == professor_data["cpf"]


@pytest.mark.django_db
def test_cpf_unique():
    Professor.objects.create(name="Prof. Carlos", email="carlos@example.com", cpf="11122233344")

    with pytest.raises(ValidationError):
        professor = Professor(name="Prof. Carlos", email="carlos2@example.com", cpf="11122233344")
        professor.full_clean()


@pytest.mark.django_db
def test_cpf_length():
    with pytest.raises(ValidationError):
        professor = Professor(name="Prof. Joana", email="joana@example.com", cpf="123456789")
        professor.full_clean()
