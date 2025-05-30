# Generated by Django 5.1.5 on 2025-01-20 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pieza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=None, max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cantidad_stock', models.IntegerField()),
                ('reorder', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MovimientoStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('tipo', models.CharField(choices=[('entrada', 'Entrada'), ('salida', 'Salida')], max_length=20)),
                ('cantidad', models.IntegerField()),
                ('pieza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pieza.pieza')),
            ],
        ),
    ]
