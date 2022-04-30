from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=255)
    nutrients = models.TextField()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "foods"

    def __str__(self):
        return self.name


class Nutrients(models.Model):
    nutrients = models.TextField()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "nutrients"

    def __str__(self):
        return self.nutrients


class Search(models.Model):
    choices = (
        ('SR Legacy', 'SR Legacy'),
        ('Branded Foods', 'Branded Foods')
    )
