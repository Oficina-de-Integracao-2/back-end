# Generated by Django 5.0.3 on 2024-04-10 21:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("oficina", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="oficina",
            name="fk",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="oficinas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
