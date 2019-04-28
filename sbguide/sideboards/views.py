from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from .forms import SideboardForm 
from .models import Sideboard, SideboardItem


class SideboardListView(ListView):

    def get_queryset(self):
        deck_slug = self.kwargs['deck']
        return Sideboard.objects.filter(deck__slug=deck_slug).order_by("opponent__deck_name")


class SideboardDetailView(DetailView):
    model = Sideboard


class SideboardCreateView(CreateView):
    model = Sideboard
    form_class = SideboardForm

    def form_valid(self, form):
        self.object = form.save()
        Sideboard.objects.filter(id=self.object.id).update(owner=self.request.user)
        return super().form_valid(form)
