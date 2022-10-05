from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Hero(models.Model):
    name = models.CharField(max_length=50)
    hp = models.IntegerField(default=100)
    attack = models.IntegerField(default=10)
    defence = models.IntegerField(default=10)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.name}"


class Monster(models.Model):
    name = models.CharField(max_length=50)
    hp = models.IntegerField(default=100)
    attack = models.IntegerField()
    defence = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Game(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    level = models.IntegerField()
    monsters = models.ManyToManyField(Monster, through='MonsterInGame')


class MonsterInGame(models.Model):
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    amount = models.IntegerField()





