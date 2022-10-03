from django import forms

class HeroCreateForm(forms.Form):
    name = forms.CharField(max_length=50)