from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(User):
    # username = models.CharField(max_length=255)
    # password = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)
    age = models.PositiveSmallIntegerField(default=2)
