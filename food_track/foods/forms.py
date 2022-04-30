from django import forms
from .models import Search


class SearchForm(forms.Form):
    choices = (
        ('SR Legacy', 'SR Legacy'),
        ('Branded Foods', 'Branded Foods')
    )
    search = forms.CharField(max_length=100)
    brand_type = forms.CharField(widget=forms.RadioSelect(choices=choices))
