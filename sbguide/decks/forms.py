from django.forms import ModelForm
from django.forms import FileField, CharField, Textarea
from .models import Deck

class DeckForm(ModelForm):
    deck_items_file = FileField(required=False, help_text="Import deck from file, for format see Mtg Goldfish deck export")
    deck_items_text = CharField(required=False, widget=Textarea, help_text="enter card quanity card name one card per line, leave any empty line for sideboard card. \n4 Lightning Bolt\n\n2 Rest in Peace" )
    
    class Meta:
        model = Deck
        fields = ['deck_name', 'archetype', 'legality', 'deck_items_file', 'deck_items_text']