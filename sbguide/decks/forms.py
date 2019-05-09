from django.forms import ModelForm
from django.forms import FileField, CharField, Textarea
from .models import Deck

class DeckForm(ModelForm):
    deck_items_file = FileField(required=False)
    deck_items_text = CharField(required=False, widget=Textarea)
    
    class Meta:
        model = Deck
        fields = ['deck_name', 'archetype', 'legality', 'deck_items_file', 'deck_items_text']