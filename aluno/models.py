from django.core.exceptions import ValidationError
from django.db import models


def validate_cpf_length(value):
    if len(value) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_cpf_length],
        help_text="Informe um CPF com exatamente 11 dígitos."
    )
    email = models.EmailField(unique=True)
