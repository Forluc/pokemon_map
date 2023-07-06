from django.db import models


class Pokemon(models.Model):
    title = models.CharField("Имя покемона", max_length=200)
    title_en = models.CharField("Имя покемона на английском", max_length=200, blank=True)
    title_jp = models.CharField("Имя покемона на японском", max_length=200, blank=True)
    photo = models.ImageField("Загрузите фото покемона", null=True, blank=True)
    description = models.TextField("Описание покемона", blank=True)
    previous_evolution = models.ForeignKey("self", verbose_name='Из кого эволюционировал', on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name='next_evolution')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='Имя покемона', on_delete=models.CASCADE, related_name='entities')
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Дата появления покемона', null=True, blank=True)
    disappeared_at = models.DateTimeField('Дата исчезновения покемона', null=True, blank=True)
    level = models.IntegerField('Уровень')
    health = models.IntegerField('Здоровье')
    strength = models.IntegerField('Сила')
    defence = models.IntegerField('Защита')
    stamina = models.IntegerField('Выносливость')

    def __str__(self):
        return f'{self.pokemon} находится в точке {self.lat}-{self.lon}'
