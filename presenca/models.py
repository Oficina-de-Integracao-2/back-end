from django.db import models
from aluno.models import Aluno
from oficina.models import Oficina


class Presenca(models.Model):
    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE,
        related_name="presencas"
    )
    oficina = models.ForeignKey(
        Oficina,
        on_delete=models.CASCADE,
        related_name="presencas"
    )
    presente = models.BooleanField(default=False)

    class Meta:
        unique_together = ('aluno', 'oficina')
