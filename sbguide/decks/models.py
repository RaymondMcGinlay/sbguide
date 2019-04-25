from django.db import models
import urllib

# Create your models here.
class Deck(models.Model):
    ARCHETYPE_CHOICES = (
        ("AGGRO", "Aggro"),
        ("COMBO", "Combo"),
        ("CONTROL", "Control"),
        ("Midrange", "Midrange"),
        ("Tempo", "Tempo"),
        ("OTHER", "Other"),
    )
    LEGALITY_CHOICES = (
        ("STANDARD", "Standard"),
        ("MODERN", "Modern"),   
    )
    deck_name = models.CharField(max_length=255)
    archetype = models.CharField(max_length=200, choices=ARCHETYPE_CHOICES)
    legality = models.CharField(max_length=200, choices=LEGALITY_CHOICES)

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