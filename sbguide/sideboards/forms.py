from django.forms import ModelForm, ModelChoiceField
from dal import autocomplete
from cards.models import Card
from .models import SideboardItem, Sideboard


class SideboardForm(ModelForm):
    
    class Meta:
        model = Sideboard
        fields = ['deck', 'opponent', 'owner']


class SideboardItemForm(ModelForm):

    class Meta:
        model = SideboardItem
        fields = ['card', 'delta', 'sideboard']
        widgets = {
            'card': autocomplete.ModelSelect2(url='card-autocomplete',
            attrs={'data-minimum-input-length': 3})
        }
    
     
