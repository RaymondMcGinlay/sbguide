from django.forms import ModelForm, ModelChoiceField
from dal import autocomplete
from cards.models import Card
from decks.models import Deck
from .models import SideboardItem, Sideboard


class SideboardForm(ModelForm):

    class Meta:
        model = Sideboard
        fields = ['deck', 'opponent', 'owner']

    def __init__(self, *args, **kwargs):
        deck = None
        if kwargs.get("deck", False):
            deck_slug = kwargs.pop('deck')
            deck = Deck.objects.get(slug=deck_slug)
        super(SideboardForm, self).__init__(*args, **kwargs)
        if deck:
            self.fields['opponent'].queryset =  Deck.objects.filter(legality=deck.legality).all()
        else:
            self.fields['opponent'].queryset =  Deck.objects.all()


class SideboardItemForm(ModelForm):

    class Meta:
        model = SideboardItem
        fields = ['card', 'delta', 'sideboard']
        widgets = {
            'card': autocomplete.ModelSelect2(url='card-autocomplete',
            attrs={'data-minimum-input-length': 3})
        }
    
     
