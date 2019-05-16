from django.urls import path
from .views import (
    SideboardDetailView,
    SideboardListView,
    SideboardsListView,
    SideboardCreateView,
    SideboardItemCreateView,
    print_decklist,
)

urlpatterns = [
    path('', SideboardsListView.as_view(), name='sideboards-list'),
    path('create/', SideboardCreateView.as_view(), name='sideboard-create'),
    path('<deck>/', SideboardListView.as_view(), name='sideboard-list'),
    path('<deck>/pdf/', print_decklist, name='sideboard-list-print'),
    path('<slug:slug>/detail/', SideboardDetailView.as_view(), name='sideboard-detail'),
    path('<slug:slug>/edit/', SideboardItemCreateView.as_view(), name='sideboard-edit'),
]