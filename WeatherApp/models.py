from django.db import models


class City(models.Model):
    Id = models.AutoField(primary_key=True)
    Address = models.CharField(max_length=25)
    Dt = models.PositiveIntegerField()

    def __str__(self):
        return self.Address

    class Meta:
        verbose_name_plural = 'cities'
