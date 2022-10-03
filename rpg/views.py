from django.shortcuts import render, redirect
from django.views import View

from rpg.forms import HeroCreateForm
from rpg.models import Hero


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'base.html')


class CreateHeroView(View):

    def get(self, request):
        form = HeroCreateForm()
        return render(request, 'create_hero.html', {'formularz':form})

    def post(self, request):
        form = HeroCreateForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            Hero.objects.create(name=name)
            return redirect('create_hero')
        return render(request, 'create_hero.html', {'formularz': form})

