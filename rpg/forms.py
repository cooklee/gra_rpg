from django import forms
from django.contrib.auth.models import User

from rpg.models import Monster


class HeroCreateForm(forms.Form):
    name = forms.CharField(max_length=50)


class MonsterCreateForm(forms.ModelForm):

    class Meta:
        model = Monster
        fields = '__all__'


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='re-Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }