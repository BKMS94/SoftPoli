# Generated by Django 5.1.6 on 2025-02-15 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('servicio', '0003_alter_servicio_kilomentraje_diff'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicio',
            old_name='kilomentraje_act',
            new_name='kilometraje_act',
        ),
        migrations.RenameField(
            model_name='servicio',
            old_name='kilomentraje_diff',
            new_name='kilometraje_diff',
        ),
    ]
