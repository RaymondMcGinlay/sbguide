from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from decks.models import Deck, DeckListItem
from decks.forms import DeckForm

class DeckListView(ListView):

    model = Deck
    paginate_by = 100

    def get_queryset(self):
        return Deck.objects.filter(owner=None)



class MyDeckListView(ListView):

    model = Deck
    paginate_by = 100

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DeckForm
        return context

class DeckDetailView(DetailView):
    model = Deck

    def get_queryset(self):
        return Deck.objects.filter(owner=None)

class MyDeckDetailView(DetailView):
    model = Deck

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)

class AddDeck(CreateView):
    form_class = DeckForm
    model = Deck

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        deck = self.object
        deck_items = form.fields['deck_items_file']
        myfile = self.request.FILES.get('deck_items_file', False)
        Deck.objects.import_from_file(deck, myfile)
        success_url = deck.get_absolute_url()
        return HttpResponseRedirect(success_url)
