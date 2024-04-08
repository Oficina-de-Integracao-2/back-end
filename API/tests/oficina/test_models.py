import pytest
from professor.models import Professor
from oficina.models import Oficina


@pytest.mark.django_db
def test_create_oficina():
    professor = Professor.objects.create(name="Dr. Ana Silva", email="anasilva@example.com", cpf="12345678901")
    oficina = Oficina.objects.create(
        title="Workshop de Python",
        description="Aprenda Python básico.",
        fk=professor
    )

    assert Oficina.objects.count() == 1, "Deveria existir apenas uma oficina registrada."
    assert oficina.title == "Workshop de Python", "O título da oficina não corresponde ao esperado."
    assert oficina.description == "Aprenda Python básico.", "A descrição da oficina não corresponde ao esperado."
    assert oficina.fk == professor, "A oficina não está corretamente associada ao professor."


@pytest.mark.django_db
def test_oficina_link_to_professor():
    professor1 = Professor.objects.create(name="Dr. Carlos Menezes", email="carlosm@example.com", cpf="98765432100")
    oficina1 = Oficina.objects.create(title="Seminário de IA", fk=professor1)

    professor2 = Professor.objects.create(name="Dr. Joana Dias", email="joanadias@example.com", cpf="12345098765")
    oficina2 = Oficina.objects.create(title="Workshop de ML", fk=professor2)

    assert oficina1.fk == professor1, "Oficina1 deveria estar associada a Professor1."
    assert oficina2.fk == professor2, "Oficina2 deveria estar associada a Professor2."

    assert professor1.oficinas.count() == 1, "Professor1 deveria ter exatamente uma oficina associada."
    assert professor2.oficinas.count() == 1, "Professor2 deveria ter exatamente uma oficina associada."
    assert professor1.oficinas.first() == oficina1, "A primeira oficina associada ao Professor1 não é a esperada."
    assert professor2.oficinas.first() == oficina2, "A primeira oficina associada ao Professor2 não é a esperada."
