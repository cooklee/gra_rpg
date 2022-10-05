"""gra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rpg import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('create_hero/', views.CreateHeroView.as_view(), name='create_hero'),
    path('create_monster/', views.AddMonsterView.as_view(), name='create_monster'),
    path('all_heroes/', views.HeroListView.as_view(), name='hero_list'),
    path('all_monsters/', views.MonsterListView.as_view(), name='monster_list'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('create_game/', views.CreateGameView.as_view(), name='create_game'),
    path('login/', views.LoginView.as_view(), name='login'),
]
