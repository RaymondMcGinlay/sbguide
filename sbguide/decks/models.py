from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
import urllib
from cards.models import Card




class DeckManager(models.Manager):
    
    def import_from_file(self, deck, decklist, update=False):
        decklist_array = []
        for line in decklist.readlines(): 
            decklist_array.append(line.decode())
        is_sideboard = False
        self.add_cards(deck, decklist_array, update)

    def import_from_text(self, deck, text, update=False):
        decklist_array = text.splitlines()
        self.add_cards(deck, decklist_array, update)
    
    
    def add_cards(self, deck, decklist_array, update):
        is_sideboard = False
        update_cards = []
        for card in decklist_array: 
            parts = card.split() 
            if len(parts) > 1: 
                quantity = parts[0] 
                name = " ".join(parts[1:]) 
                print(name)
                card_result = Card.objects.find_card(name=name)
                if card_result['status'] in ['exact', 'partial']:
                    card = card_result['card']
                elif card_result['status'] in ['partial-multi']:
                    card = card_result['card'][0]
                if card_result['status'] == "not-found":
                    print("error")
                    card = None
                if card:
                    if update:
                        dlt = DeckListItem.objects.filter(deck=deck, card=card, is_sideboard=is_sideboard).update(quantity=quantity)
                        if dlt:
                            decklistitem = DeckListItem.objects.get(deck=deck, card=card, is_sideboard=is_sideboard)
                        else:
                            decklistitem = DeckListItem.objects.create(deck=deck, card=card, is_sideboard=is_sideboard, quantity=quantity)
                        update_cards.append(decklistitem.id)
                    else:    
                        decklistitem = DeckListItem.objects.create(deck=deck, card=card, is_sideboard=is_sideboard, quantity=quantity)
            else: 
                is_sideboard = True
            if update:
                # delete any removed cards
                DeckListItem.objects.filter(deck=deck).exclude(id__in=update_cards).delete()




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
    slug = models.SlugField()
    archetype = models.CharField("Archetype", max_length=200, choices=ARCHETYPE_CHOICES)
    legality = models.CharField("Format", max_length=200, choices=LEGALITY_CHOICES)
    emblem = models.ForeignKey('cards.card', related_name='emblem_card', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), related_name="deck_owner", blank=True, null=True, on_delete=models.CASCADE)
    is_empty = models.BooleanField(default=False, help_text="An empty deck is used to represent an opponents deck, it has no cards")
    objects = DeckManager()

    def save(self, *args, **kwargs):
        if self.owner:
            slug = "%s-%s" % (self.deck_name, self.owner.id*12543)
        else:
            slug = self.deck_name
        self.slug = slugify(slug)
        super(Deck, self).save(*args, **kwargs)
    class Meta:
        ordering = ['deck_name']

    def get_card_objects(self):
        return DeckListItem.objects.filter(deck=self)

    def get_mainboard_cards(self):
        return [{'qty': d.quantity, 'card' :d.card.name, 'id': d.card.id} for d in DeckListItem.objects.filter(deck=self, is_sideboard=False)]

    def get_sideboard_cards(self):
        return [{'qty': d.quantity, 'card' :d.card.name, 'id': d.card.id} for d in DeckListItem.objects.filter(deck=self, is_sideboard=True)]

    def get_decklist_str(self):
        mb = self.get_mainboard_cards()
        sb = self.get_sideboard_cards()
        mb_string="".join([urllib.parse.quote("%s %s" % (c['qty'], c['card']))+"%0A" for c in mb])
        sb_string="".join([urllib.parse.quote("%s %s" % (c['qty'], c['card']))+"%0A" for c in sb])   
        return "deckmain=%s&deckside=%s" % (mb_string, sb_string)
    
    def deck_items_text(self):
        dlt = ""
        for d in DeckListItem.objects.filter(deck=self, is_sideboard=False).order_by('card'):
            dlt += "%s %s\n" % (d.quantity, d.card.name)
        dlt += "\n"
        for d in DeckListItem.objects.filter(deck=self, is_sideboard=True).order_by('card'):
            dlt += "%s %s\n" % (d.quantity, d.card.name)
        return dlt
        


    def get_absolute_url(self):
        if not self.owner:
            return reverse('deck-detail', args=[str(self.slug)])
        else:
            return reverse('mydeck-detail', args=[str(self.slug)])
    
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