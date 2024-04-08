from django.core.exceptions import ValidationError
from django.db import models


def validate_cpf_length(value):
    if len(value) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")


class Professor(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf_length])
