from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField("Имя покемона", max_length=200)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    Pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    Lat = models.FloatField()
    Lon = models.FloatField()

    def __str__(self):
        return f'{self.Pokemon} находится в точке {self.Lat}-{self.Lon}'
