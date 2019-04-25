from django.contrib import admin
from .models import Deck, DeckListItem

class DecklistItemline(admin.TabularInline):
    model = DeckListItem
    raw_id_fields = ('card',)

class DeckAdmin(admin.ModelAdmin):
    list_display = ('deck_name', 'archetype', 'legality')
    list_display_links = ('deck_name',)
    search_fields = ('deck_name',)
    list_filter = ('archetype', 'legality')
    inlines = [DecklistItemline,]
    raw_id_fields = ('emblem',)

admin.site.register(Deck, DeckAdmin)
