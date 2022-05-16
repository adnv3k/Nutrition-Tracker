from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=255)
    nutrients = models.TextField()
    dataType = models.CharField(max_length=15, default='SR Legacy')
    brandOwner = models.CharField(max_length=255, default=False)
    favorite = models.ManyToManyField(User, related_name='favorite_food')
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
    date = models.DateTimeField(auto_now=True)
    food = models.CharField(max_length=255)
    food_id = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.username

class SRLegacy(models.Model):
    name = models.CharField(max_length=255)
    fdc_id = models.IntegerField()
    category = models.CharField(max_length=255)
    publication_date = models.DateField()
    nutrients = models.TextField()
    objects = models.Manager()

class Branded(models.Model):
    brandOwner = models.CharField(max_length=255, default=False)
    name = models.TextField()
    fdc_id = models.IntegerField()
    category = models.TextField()
    publication_date = models.DateField()
    marketCountry = models.CharField(max_length=255)
    nutrients = models.TextField()
    ingredients = models.TextField()
    objects = models.Manager()
