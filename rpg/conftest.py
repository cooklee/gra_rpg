import pytest

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