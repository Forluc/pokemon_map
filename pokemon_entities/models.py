from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField("Имя покемона", max_length=200)
    title_en = models.CharField("Имя покемона на английском", max_length=200, blank=True)
    title_jp = models.CharField("Имя покемона на японском", max_length=200, blank=True)
    photo = models.ImageField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities')
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()

    def __str__(self):
        return f'{self.pokemon} находится в точке {self.lat}-{self.lon}'
