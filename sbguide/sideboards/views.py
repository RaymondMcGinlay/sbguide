from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Sideboard

class SideboardDetailView(DetailView):
    model = Sideboard
