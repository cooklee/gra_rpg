from random import choice

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from rpg.forms import HeroCreateForm, MonsterCreateForm, CreateUserForm, LoginForm
from rpg.models import Hero, Monster, Game, Stage, AlavieMonsterInStage, AliveMonster


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'base.html')


class HeroListView(View):

    def get(self, request):
        heroes = Hero.objects.all()
        return render(request, 'hero_list.html', {'heroes': heroes})


class MyHeroListView(LoginRequiredMixin, View):

    def get(self, request):
        heroes = Hero.objects.filter(owner=request.user)
        return render(request, 'hero_list.html', {'heroes': heroes})


class CreateHeroView(LoginRequiredMixin, View):  # LoginRequiredMixin pozwala wejść tylko zalogowanym użytkowniką
    # musi być pierwszą klasą z której dziedziczymy
    def get(self, request):
        form = HeroCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = HeroCreateForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            Hero.objects.create(name=name, owner=request.user)
            return redirect('create_hero')
        return render(request, 'form.html', {'form': form})


class AddMonsterView(UserPassesTestMixin, View):

    def test_func(self):  # funkcja musi nazywać sie test_func
        return self.request.user.is_superuser

    def get(self, request):
        form = MonsterCreateForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = MonsterCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('create_monster')
        return render(request, 'form.html', {'form': form})


class MonsterListView(PermissionRequiredMixin, View):
    permission_required = ['rpg.change_monster']

    def get(self, request):
        monster = Monster.objects.all()
        return render(request, 'hero_list.html', {'heroes': monster})


class CreateUserView(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)  # pobiera dane wysłane postem i na  ich podstawie
        # wypełnia forlmularz CreateUserForm

        if form.is_valid():  # nastepuje validacja formlarza czyli validowane sa wszystkie pola
            # a następnie wywołana metoda clean w formularzu
            user = form.save(
                commit=False)  # commit = False powoduje ze nie zostanie CAŁY obiekt zapisany do bazy danych

            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('create_monster')
        return render(request, 'form.html', {'form': form})


class CreateGameView(LoginRequiredMixin, CreateView):
    model = Game
    template_name = 'form.html'
    success_url = '/'
    fields = ['hero', 'level']


class CreateGameForHero(LoginRequiredMixin, View):

    def get(self, request, id_hero):
        hero = Hero.objects.get(pk=id_hero)  # pobranie bochatera o id id_hero
        game = Game.objects.create(hero=hero, level=1)
        stage = Stage.objects.create(game=game, level=2)
        stage = Stage.objects.create(game=game, next_stage=stage)
        url = reverse('stage_detail', args=(stage.id,))
        return redirect(url)


class GameDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        game = Game.objects.get(pk=pk)
        return render(request, 'game_detail.html', {'game': game})


class FightView(LoginRequiredMixin, View):
    def get(self, request, stage_id):
        stage = Stage.objects.get(pk=stage_id)
        monsters = stage.monsters.filter(current_hp__gt=0)
        hero = stage.game.hero
        if monsters.count() > 0:
            target = choice(monsters)
            dm = hero.attack - target.defence
            if dm <= 0:
                dm = 1
            target.current_hp -= dm
            target.save()
            monster_dmg = 0
            for monster in monsters:
                dm = monster.attack - hero.defence
                if dm <= 0:
                    dm = 1
                monster_dmg += dm
            hero.hp -= dm
            hero.save()
        url = reverse('stage_detail', args=(stage_id,))
        return redirect(url)


class StageDetailView(LoginRequiredMixin, View):

    def get(self, request, pk):
        stage = Stage.objects.get(pk=pk)
        if stage.next_stage is None:
            stage.next_stage = Stage.objects.create(game=stage.game, level=stage.level + 1)
        if not stage.visited:
            stage.generate_monster()
            stage.visited = True
            stage.save()
        return render(request, 'stage_detail.html', {'stage': stage})


class AttackMonsterView(View):

    def get(self, request, monster_id, hero_id):
        monster = AliveMonster.objects.get(pk=monster_id)
        hero = Hero.objects.get(pk=hero_id)
        dmg = hero.attack - monster.defence
        if dmg <= 0:
            dmg = 1
        monster.current_hp -= dmg
        monster.save()
        if monster.current_hp > 0:
            dmg = monster.attack - hero.defence
            if dmg <= 0:
                dmg = 1
            hero.hp -= dmg
        else:
            hero.attack += monster.attack
        hero.save()
        stage = monster.stage_set.first()
        return redirect('stage_detail', stage.id)


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            us = form.cleaned_data['username']
            pd = form.cleaned_data['password']
            user = authenticate(username=us, password=pd)
            if user is None:
                return render(request, 'form.html', {'form': form, 'message': "Niepoprawne dane"})
            else:
                login(request, user)
                url = request.GET.get('next', 'index')
                return redirect(url)
        return render(request, 'form.html', {'form': form, 'message': "Niepoprawne dane"})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('index')
