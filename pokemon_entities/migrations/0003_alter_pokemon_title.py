# Generated by Django 3.2.19 on 2023-07-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_pokemon_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Имя покемона'),
        ),
    ]
