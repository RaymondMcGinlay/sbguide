from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from decks.models import Deck

class DeckListView(ListView):

    model = Deck
    paginate_by = 100

class DeckDetailView(DetailView):
    model = Deck