from django.db import models
from django.utils.safestring import mark_safe
from .utils import parse_card_json, get_set

class CardManager(models.Manager):
    
    def add_card_from_json(self, card, save=True):
        data = parse_card_json(card)
        if save:
            if Card.objects.filter(name = data['name']).exists():
                Card.objects.filter(name = data['name']).update(**data)
            else:
                Card.objects.get_or_create(**data)
        else:
            return data


    def add_set(self, set_code, url=None, save=True):
        if url:
            set_json = get_set(set_code, url)
        else:
            set_json = get_set(set_code)
        for card in set_json['data']:
            card  = self.add_card_from_json(card, save=save)
        if set_json['has_more']:
            self.add_set(set_code,url=set_json['next_page'], save=save)

    def find_card(self, name):
        """
            first try perfect match 
        """
        try:
            return {"status": "exact", "card": Card.objects.get(name_iexact=name)}
        except:
            pass
        # split multi faced card 
        name = name.split("/")[0]
        startswithsearch = Card.objects.filter(name__istartswith=name)
        if len(startswithsearch) == 1:
            """ card partially matches with a single hit"""
            return {"status": "partial", "card": startswithsearch.first()}
        elif len(startswithsearch) > 1:
            """ card partially matches with a single hit"""
            return {"status": "partial-multi", "card": startswithsearch}
        contains_search = Card.objects.filter(name__icontains=name)
        if len(contains_search) == 1:
            """ card partially matches with a single hit"""
            return {"status": "partial", "card": contains_search.first()}
        elif len(contains_search) > 1:
            """ card partially matches with a single hit"""
            return {"status": "partial-multi", "card": contains_search}

        return {"status": "not-found", 'card': None}

        




# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=255)
    scryfall_id = models.CharField(max_length=255, blank=True, null=True)
    type_line = models.CharField(max_length=255, blank=True, null=True)
    set_code = models.CharField(max_length=255)
    image_link = models.URLField()
    mana_cost = models.CharField(max_length=255, blank=True, null=True)
    standard_legal = models.BooleanField()
    modern_legal = models.BooleanField()
    objects = CardManager()
    
    def image_tag(self):
        if self.image_link:
            return mark_safe('<img src="%s" width="25%" height="25%" />' % self.image_link)
        else:
            return ""
    @property
    def image_art_crop(self):
        return self.image_link.replace('normal', 'art_crop')
    
    @property
    def image_small(self):
        return self.image_link.replace('normal', 'small')


    def __str__(self):
        return self.name 

    def __unicode__(self):
        return self.name
