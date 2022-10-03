from django.shortcuts import render
from django.views import View

from rpg.forms import HeroCreateForm


# Create your views here.

class IndexView(View):

    def get(self, request):
        return render(request, 'base.html')


class CreateHeroView(View):

    def get(self, request):
        form = HeroCreateForm()
        return render(request, 'create_hero.html', {'formularz':form})
