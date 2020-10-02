from django.db import models


class City(models.Model):
    Address = models.CharField(max_length=25)

    def __str__(self):
        return self.Address

    class Meta:
        verbose_name_plural = 'cities'
