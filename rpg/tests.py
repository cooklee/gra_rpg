from django.test import Client


def test_index():
    clinet = Client()
    url = '/'
    response = clinet.get(url)
    assert response.status_code == 200
    assert 'gra rpg' in str(response.content)