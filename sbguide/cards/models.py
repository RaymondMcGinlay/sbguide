from django.db import models
from django.utils.safestring import mark_safe
from .utils import parse_card_json, get_set

class CardManager(models.Manager):
    
    def add_card_from_json(self, card, save=True):
        data = parse_card_json(card)
        if save:
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





# Create your models here.
class Card(models.Model):
    name = models.CharField(max_length=255)
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


    def __str__(self):
        return self.name 

    def __unicode__(self):
        return self.name
