from django.urls import path
from .views import DeckListView, DeckDetailView

urlpatterns = [
    path('', DeckListView.as_view(), name='deck-list'),
    path('<slug:pk>/', DeckDetailView.as_view(), name='deck-detail'),
]