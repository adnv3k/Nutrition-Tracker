from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=255)
    nutrients = models.TextField()
    dataType = models.CharField(max_length=15, default='SR Legacy')
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


class FoodHistory(models.Model):
    username = models.CharField(max_length=255)
    food = models.CharField(max_length=255)
    nutrients = models.TextField()
    date = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.username
