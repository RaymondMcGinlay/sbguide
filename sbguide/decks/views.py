from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from decks.models import Deck, DeckListItem
from decks.forms import DeckForm
from cards.models import Card
from django.contrib.auth.mixins import LoginRequiredMixin

class DeckListView(ListView):

    model = Deck
    paginate_by = 100

    def get_queryset(self):
        legality = self.kwargs.get('format', False)
        if legality:
            return Deck.objects.filter(owner=None, legality=legality.upper())
        return Deck.objects.filter(owner=None)



class MyDeckListView(LoginRequiredMixin, ListView):

    model = Deck
    paginate_by = 100

    def get_queryset(self):
        user = self.request.user
        legality = self.kwargs.get('format', False)
        if legality:
            return Deck.objects.filter(owner=user, legality=legality.upper())
        return Deck.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DeckForm
        return context

class DeckDetailView(DetailView):
    model = Deck

    def get_queryset(self):
        return Deck.objects.filter(owner=None)

class MyDeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)
    
    def get(self, request, *args, **kwargs):
        c = request.GET.get('c', '')
        deck = self.get_object()
        if c:
            card = Card.objects.get(id=c)
            deck.emblem = card
            deck.save()
        return super().get(request, *args, **kwargs)


class AddDeck(CreateView):
    form_class = DeckForm
    model = Deck

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        deck = self.object
        deck_items_text = form.fields['deck_items_text']
        myfile = self.request.FILES.get('deck_items_file', False)
        if myfile:
            Deck.objects.import_from_file(deck, myfile)
        elif deck_items_text:
            Deck.objects.import_from_text(deck, form.cleaned_data['deck_items_text'])
        success_url = deck.get_absolute_url()
        return HttpResponseRedirect(success_url)
