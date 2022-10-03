import pytest
from django.test import Client
from django.urls import reverse

from rpg.forms import HeroCreateForm
from rpg.models import Hero


def test_index():
    client = Client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200
    assert 'gra rpg' in str(response.content)


def test_add_hero_get():
    client = Client() # otwórz przeglądarke
    url = reverse('create_hero') # znajdz url o nazwie create_hero
    response = client.get(url) # wejdz metodą get nasza symulacyjną przegladarka na tego URL
    assert response.status_code == 200
    form_in_view = response.context['formularz'] # pobierz z kontekstu zmienną o nazwie formularz
    assert isinstance(form_in_view, HeroCreateForm)

@pytest.mark.django_db # ten dekorator mowi temu testowi wolno dotykać bazy danych
def test_add_hero_post():
    client = Client() # otwórz przeglądarke
    url = reverse('create_hero') # znajdz url o nazwie create_hero
    data = {     # wpisz w formularzy w pole name wartość slawek
        'name':'slawek',
    }
    response = client.post(url, data) # wejdz metodą post nasza symulacyjną przegladarka na tego URL
    assert response.status_code == 302 # bo w widoku jest redirect
    assert Hero.objects.get(name='slawek') # sprawdz czy slawek jest w bazie danych

