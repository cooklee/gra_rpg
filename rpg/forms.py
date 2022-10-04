from django import forms

from rpg.models import Monster


class HeroCreateForm(forms.Form):
    name = forms.CharField(max_length=50)


class MonsterCreateForm(forms.ModelForm):

    class Meta:
        model = Monster
        fields = '__all__'