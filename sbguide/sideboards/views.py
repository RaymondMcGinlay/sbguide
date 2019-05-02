from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.urls import reverse
from .forms import SideboardForm, SideboardItemForm
from .models import Sideboard, SideboardItem
from decks.models import Deck
from cards.models import Card
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

    def get_success_url(self):
        sb_slug = self.kwargs['slug']
        sideboard = Sideboard.objects.get(slug=sb_slug)
        return reverse('sideboard-edit', kwargs={'slug': sideboard.slug})

    def get_context_data(self, **kwargs):
        sb_slug = self.kwargs['slug']
        sideboard = Sideboard.objects.get(slug=sb_slug)
        context = super().get_context_data(**kwargs)
        context["form"] = SideboardItemForm(initial={
            'sideboard': sideboard
            })
        context["object"] = sideboard
        return context

    def form_valid(self, form):
        """If objects exists change delta."""
        self.object = form.save()
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        sb_slug = self.kwargs['slug']
        sideboard = Sideboard.objects.get(slug=sb_slug)
        c = request.GET.get('c', '')
        p = request.GET.get('p', '')
        m = request.GET.get('m', '')
        if c and (m or p):
            card = Card.objects.get(id=c)
            sideboarditem, created = SideboardItem.objects.get_or_create(
                sideboard = sideboard,
                card = card
            )
            if p:
                delta = sideboarditem.delta+1
                if delta < 5:
                    sideboarditem.delta = delta
                    sideboarditem.save()
            if m:
                delta = sideboarditem.delta-1
                if delta > -5:
                    sideboarditem.delta = delta
                    sideboarditem.save()
        self.object = None
        return super().get(request, *args, **kwargs)
    
