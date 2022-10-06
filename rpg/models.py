from random import randint, choice

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


class AliveMonster(models.Model):
    monster_class = models.ForeignKey(Monster, on_delete=models.CASCADE)
    current_hp = models.IntegerField(null=True)

    @property
    def attack(self):
        return self.monster_class.attack

    @property
    def defence(self):
        return self.monster_class.defence

    @property
    def name(self):
        return self.monster_class.name


class Game(models.Model):
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)
    level = models.IntegerField()
    monsters = models.ManyToManyField('AliveMonster', through='AlavieMonsterInGame')


class Stage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    monsters = models.ManyToManyField(AliveMonster, through='AlavieMonsterInStage')
    visited = models.BooleanField(default=False)

    def generate_monster(self):
        monster_list = Monster.objects.all()
        amount = randint(0, 5)
        for _ in range(amount):
            mc = choice(monster_list)
            am = AliveMonster.objects.create(monster_class=mc, current_hp=mc.hp)
            AlavieMonsterInStage.objects.create(stage=self, monster=am)


class AlavieMonsterInGame(models.Model):
    monster = models.ForeignKey(AliveMonster, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class AlavieMonsterInStage(models.Model):
    monster = models.ForeignKey(AliveMonster, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
