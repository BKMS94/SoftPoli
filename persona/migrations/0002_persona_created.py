# Generated by Django 5.1.5 on 2025-01-20 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
