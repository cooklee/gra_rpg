from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Hero(models.Model):
    name = models.CharField(max_length=50)
    hp = models.IntegerField(default=100)
    attack = models.IntegerField(default=10)
    defence = models.IntegerField(default=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
