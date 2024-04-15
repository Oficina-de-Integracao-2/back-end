from django.db import models


class Oficina(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)

    professor = models.ForeignKey(
        "professor.Professor",
        on_delete=models.CASCADE,
        related_name="oficinas"
    )
