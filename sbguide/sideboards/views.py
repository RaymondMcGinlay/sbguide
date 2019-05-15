from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from weasyprint import HTML
from weasyprint.fonts import FontConfiguration

from cards.models import Card
from decks.models import Deck, DeckListItem

from .forms import SideboardForm, SideboardItemForm
from .models import Sideboard, SideboardItem



class SideboardsListView(ListView):
    template_name = "sideboards/sideboards_list.html"

    def get_queryset(self):
        Sideboard.objects.order_by('pub_date').distinct('pub_date')
        return Sideboard.objects.order_by('deck__deck_name').distinct('deck__deck_name')


class SideboardListView(ListView):

    def get_queryset(self):
        deck_slug = self.kwargs['deck']
        return Sideboard.objects.filter(deck__slug=deck_slug).order_by("opponent__deck_name")

    
    def get_context_data(self, **kwargs):
        deck_slug = self.kwargs['deck']
        deck = Deck.objects.get(slug=deck_slug)
        context = super().get_context_data(**kwargs)
        decks = Deck.objects.filter(legality=deck.legality)
        context['form'] = SideboardForm(initial={
            'deck': deck,
            'owner': self.request.user,
            }, deck=deck_slug)
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
                if sideboarditem.delta < 0:
                    is_sideboard = False
                else:
                    is_sideboard = True 
                deck_qty = DeckListItem.objects.get(deck=sideboard.deck, card=card, is_sideboard=is_sideboard).quantity
                delta = sideboarditem.delta+1
                if delta <= deck_qty:
                    sideboarditem.delta = delta
                    sideboarditem.save()
            if m:
                if sideboarditem.delta > 0:
                    is_sideboard = True
                else:
                    is_sideboard = False
                deck_qty = DeckListItem.objects.get(deck=sideboard.deck, card=card, is_sideboard=is_sideboard).quantity
                delta = sideboarditem.delta-1
                if delta >= -deck_qty:
                    sideboarditem.delta = delta
                    sideboarditem.save()
        self.object = None
        return super().get(request, *args, **kwargs)
    

def print_decklist(request, deck):
    deck = Deck.objects.get(slug=deck)
    sideboards = Sideboard.objects.filter(deck=deck).order_by("opponent__deck_name")
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename={name}-sideboard-guide.pdf".format(
        name=deck.slug,
    )
    html = render_to_string("sideboards/pdf/base.html", {
        'deck': deck,
        'sideboards': sideboards
    })

    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response
