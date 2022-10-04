from django.shortcuts import render, redirect
from django.views import View

from rpg.forms import HeroCreateForm, MonsterCreateForm, CreateUserForm
from rpg.models import Hero


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'base.html')




class HeroListView(View):

    def get(self, request):
        heroes = Hero.objects.all()
        return render(request, 'hero_list.html', {'heroes':heroes})


class CreateHeroView(View):

    def get(self, request):
        form = HeroCreateForm()
        return render(request, 'form.html', {'formularz':form})

    def post(self, request):
        form = HeroCreateForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            Hero.objects.create(name=name)
            return redirect('create_hero')
        return render(request, 'form.html', {'formularz': form})

class AddMonsterView(View):

    def get(self, request):
        form = MonsterCreateForm()
        return render(request, 'form.html', {'formularz': form})

    def post(self, request):
        form = MonsterCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('create_monster')
        return render(request, 'form.html', {'formularz': form})


class CreateUserView(View):

    def get(self, request):
        form = CreateUserForm()
        return render(request, 'form.html', {'formularz': form})

    def post(self, request):
        form = CreateUserForm(request.POST) #pobiera dane wysłane postem i na  ich podstawie
        # wypełnia forlmularz CreateUserForm

        if form.is_valid(): #nastepuje validacja formlarza czyli validowane sa wszystkie pola
                            # a następnie wywołana metoda clean w formularzu
            user = form.save(commit=False) # commit = False powoduje ze nie zostanie CAŁY obiekt zapisany do bazy danych
            password = user.password
            user.set_password(password)
            user.save()
            return redirect('create_monster')
        return render(request, 'form.html', {'formularz': form})
