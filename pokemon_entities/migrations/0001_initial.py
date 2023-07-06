# Generated by Django 3.2.19 on 2023-07-06 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Имя покемона')),
                ('title_en', models.CharField(blank=True, max_length=200, verbose_name='Имя покемона на английском')),
                ('title_jp', models.CharField(blank=True, max_length=200, verbose_name='Имя покемона на японском')),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('description', models.TextField(blank=True)),
                ('previous_evolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('appeared_at', models.DateTimeField(null=True)),
                ('disappeared_at', models.DateTimeField(null=True)),
                ('level', models.IntegerField()),
                ('health', models.IntegerField()),
                ('strength', models.IntegerField()),
                ('defence', models.IntegerField()),
                ('stamina', models.IntegerField()),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='pokemon_entities.pokemon')),
            ],
        ),
    ]
