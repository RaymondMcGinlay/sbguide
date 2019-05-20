from django.urls import path
from .views import (
    DeckListView,
    DeckDetailView,
    MyDeckListView,
    MyDeckDetailView,
    AddDeckView,
    UpdateDeckView,
)

urlpatterns = [
    path('mydecks-add', AddDeckView.as_view(), name='mydeck-add'),
    path('mydecks-update/<slug:slug>/', UpdateDeckView.as_view(), name='mydeck-update'),
    path('mydecks/<slug:slug>/', MyDeckDetailView.as_view(), name='mydeck-detail'),
    path('mydecks/<format>/', MyDeckListView.as_view(), name='deck-mylist-format'),
    path('mydecks/', MyDeckListView.as_view(), name='deck-mylist'),
    path('metadecks/<slug:slug>/', DeckDetailView.as_view(), name='deck-detail'),
    path('metadecks/<format>/', DeckListView.as_view(), name='deck-list-format'),
    path('metadecks/', DeckListView.as_view(), name='deck-list'),
]