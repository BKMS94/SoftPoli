# Generated by Django 5.2 on 2025-07-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0007_vehiculo_fecha_adquisicion_vehiculo_tipo_combustible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='fecha_adquisicion',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de adquisición'),
        ),
    ]
