from django.db import models


class Oficina(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    workload = models.DecimalField(max_digits=5, decimal_places=2)
    city_of_realization = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)
    date_of_realization = models.DateField()
    time_of_realization = models.TimeField()
    realized = models.BooleanField(default=False)

    professor = models.ForeignKey(
        "professor.Professor",
        on_delete=models.CASCADE,
        related_name="oficinas"
    )
