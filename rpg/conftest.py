import pytest
from django.contrib.auth.models import User

from rpg.models import Hero


@pytest.fixture
def heroes():
    lst = []
    for x in range(10):
        lst.append(Hero.objects.create(name=x))
    return lst


@pytest.fixture
def hero():
    return Hero.objects.create(name='Thor')

@pytest.fixture
def user():
    return User.objects.create(username='test')