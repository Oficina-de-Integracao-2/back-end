from django.db import models


class Professor(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
