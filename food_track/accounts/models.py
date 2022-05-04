from django.db import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    # sex = models.CharField(max_length=1)
    # age = models.PositiveSmallIntegerField(null=0)
