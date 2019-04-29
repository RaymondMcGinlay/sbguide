from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from .forms import SideboardForm, SideboardItemForm
from .models import Sideboard, SideboardItem
from decks.models import Deck
from django.contrib.auth.mixins import LoginRequiredMixin


class SideboardListView(ListView):

    def get_queryset(self):
        deck_slug = self.kwargs['deck']
        return Sideboard.objects.filter(deck__slug=deck_slug).order_by("opponent__deck_name")
    
    def get_context_data(self, **kwargs):
        deck_slug = self.kwargs['deck']
        deck = Deck.objects.get(slug=deck_slug)
        context = super().get_context_data(**kwargs)
        context["form"] = SideboardForm(initial={
            'deck': deck,
            'owner': self.request.user
            })
        return context
    


class SideboardDetailView(DetailView):
    model = Sideboard


class SideboardCreateView(LoginRequiredMixin, CreateView):
    model = Sideboard
    form_class = SideboardForm

    def form_valid(self, form):
        self.object = form.save()
        Sideboard.objects.filter(id=self.object.id).update(owner=self.request.user)
        return super().form_valid(form)


class SideboardItemCreateView(LoginRequiredMixin, CreateView):
    model = SideboardItem
    form_class = SideboardItemForm
