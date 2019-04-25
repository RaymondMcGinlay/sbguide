from django.db import models
import urllib
from cards.models import Card


class DeckManager(models.Manager):
    
    def import_from_file(self, name, deck_file):
        decklist = open(deck_file, 'r')
        decklist_array = []
        for line in decklist.readlines(): 
            decklist_array.append(line)
        deck = Deck.objects.create(deck_name=name) 
        is_sideboard = False
        for card in decklist_array: 
            parts = card.split() 
            if len(parts) > 1: 
                quantity = parts[0] 
                name = " ".join(parts[1:]) 
                print(name) 
                card = Card.objects.get(name=name) 
                DeckListItem.objects.create(deck=deck, quantity=quantity, card=card, is_sideboard=is_sideboard) 
            else: 
                is_sideboard = True         



# Create your models here.
class Deck(models.Model):
    ARCHETYPE_CHOICES = (
        ("AGGRO", "Aggro"),
        ("COMBO", "Combo"),
        ("CONTROL", "Control"),
        ("MIDRANGE", "Midrange"),
        ("TEMPO", "Tempo"),
        ("OTHER", "Other"),
    )
    LEGALITY_CHOICES = (
        ("STANDARD", "Standard"),
        ("MODERN", "Modern"),   
    )
    deck_name = models.CharField(max_length=255)
    archetype = models.CharField(max_length=200, choices=ARCHETYPE_CHOICES)
    legality = models.CharField(max_length=200, choices=LEGALITY_CHOICES)
    emblem = models.ForeignKey('cards.card', related_name='emblem_card', on_delete=models.CASCADE)

    objects = DeckManager()

    class Meta:
        ordering = ['deck_name']

    def get_mainboard_cards(self):
        return [{'qty': d.quantity, 'card' :d.card.name} for d in DeckListItem.objects.filter(deck=self, is_sideboard=False)]

    def get_sideboard_cards(self):
        return [{'qty': d.quantity, 'card' :d.card.name} for d in DeckListItem.objects.filter(deck=self, is_sideboard=True)]

    def get_decklist_str(self):
        mb = self.get_mainboard_cards()
        sb = self.get_sideboard_cards()
        mb_string="".join([urllib.parse.quote("%s %s" % (c['qty'], c['card']))+"%0A" for c in mb])
        sb_string="".join([urllib.parse.quote("%s %s" % (c['qty'], c['card']))+"%0A" for c in sb])   
        return "deckmain=%s&deckside=%s" % (mb_string, sb_string)

    def __str__(self):
        return self.deck_name 

    def __unicode__(self):
        return self.deck_name

class DeckListItem(models.Model):
    deck = models.ForeignKey('decks.deck', related_name='decklistitem_deck', on_delete=models.CASCADE)
    card = models.ForeignKey('cards.card', related_name='decklistitem_card', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_sideboard = models.BooleanField(default=False)

    def __str__(self):
        return "%s - %sx%s" %(self.deck, self.quantity, self.card) 

    def __unicode__(self):
        return "%s - %sx%s" %(self.deck, self.quantity, self.card)