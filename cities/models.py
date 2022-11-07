from django.db import models


class City(models.Model):
    name = models.CharField(unique=True, max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"
        db_table = "cities"

    def __str__(self):
        return f"{self.name} city"
