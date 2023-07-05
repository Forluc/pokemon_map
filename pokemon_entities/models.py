from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField("Имя покемона", max_length=200)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
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
