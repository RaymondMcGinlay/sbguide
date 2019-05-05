from django.urls import path
from .views import (
    DeckListView,
    DeckDetailView,
    MyDeckListView,
    MyDeckDetailView,
    AddDeck,
)

urlpatterns = [
    path('mydecks/', MyDeckListView.as_view(), name='mydeck-list'),
    path('mydecks-add/', AddDeck.as_view(), name='mydeck-add'),
    path('mydecks/<slug:slug>/', MyDeckDetailView.as_view(), name='mydeck-detail'),
    path('metadecks/', DeckListView.as_view(), name='deck-list'),
    path('metadecks/<slug:slug>/', DeckDetailView.as_view(), name='deck-detail'),
]