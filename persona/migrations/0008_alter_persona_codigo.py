# Generated by Django 5.1.5 on 2025-01-27 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0007_rename_es_tecnico__persona_estecnico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='codigo',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
