from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.urls import reverse

def get_slug(instance):
    if instance.owner:
        return "%s-%s-%s" % (instance.owner ,instance.deck.slug, instance.opponent.slug)
    return "%s-%s" % (instance.deck.slug, instance.opponent.slug)

# Create your models here.
class Sideboard(models.Model):
    """
        Matchup between two decks
    """
    owner = models.ForeignKey(
        get_user_model(),
        related_name='sideboard_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    slug = AutoSlugField(populate_from=get_slug)
    deck = models.ForeignKey('decks.deck', related_name='sideboard_deck', on_delete=models.CASCADE)
    opponent = models.ForeignKey('decks.deck', related_name='opponent_deck', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('owner', 'deck', 'opponent')

    def __str__(self):
        return  "%s v %s" % (self.deck.deck_name, self.opponent.deck_name)

    def __unicode__(self):
        return  "%s v %s" % (self.deck.deck_name, self.opponent.deck_name)

    def get_sb_items(self):
        return SideboardItem.objects.filter(sideboard=self).order_by('card__name')
    
    def get_cards_in(self):
        return [{'qty': d.delta, 'card' :d.card.name, 'id': d.card.id} for d in self.get_sb_items() if d.delta > 0]
    
    def get_cards_out(self):
        return [{'qty': abs(d.delta), 'card' :d.card.name, 'id': d.card.id} for d in self.get_sb_items() if d.delta < 0]
    
    def check_sanity(self):
        diff = sum([sideboarditem.delta for sideboarditem in self.get_sb_items()])
        if diff == 0:
            return True
        return False
    
    def get_absolute_url(self):
        return reverse('sideboard-detail', args=[str(self.slug)])



class SideboardItem(models.Model):
    """
        Cards coming in or out represented by positive or negative integer field 2 or -2
    """
    sideboard = models.ForeignKey('sideboards.sideboard', related_name='sideboarditem_sideboard', on_delete=models.CASCADE)
    card = models.ForeignKey('cards.card', related_name='sideboarditem_card', on_delete=models.CASCADE)
    delta = models.IntegerField(default=0)

    def in_or_out(self):
        if self.delta > 0:
            return "%s in" % self.delta
        elif self.delta < 0:
            return "%s out" % self.delta
    def __str__(self):
        return  "%s  %s" % (self.card.name, self.in_or_out())

    def __unicode__(self):
        return  "%s  %s" % (self.card.name, self.in_or_out())
