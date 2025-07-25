# Generated by Django 5.2 on 2025-07-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grado', '0002_alter_grado_nombre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grado',
            options={'ordering': ['orden', 'nombre'], 'verbose_name': 'Grado', 'verbose_name_plural': 'Grados'},
        ),
        migrations.AddField(
            model_name='grado',
            name='abreviatura',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Abreviatura'),
        ),
        migrations.AddField(
            model_name='grado',
            name='orden',
            field=models.CharField(default=0, verbose_name='Orden Jerárquico'),
        ),
        migrations.AlterField(
            model_name='grado',
            name='nombre',
            field=models.CharField(max_length=50, unique=True, verbose_name=' Nombre del Grado'),
        ),
    ]
