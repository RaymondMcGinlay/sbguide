from django.urls import path
from .views import (
    SideboardDetailView,
    SideboardListView,
    SideboardsListView,
    SideboardCreateView,
    SideboardItemCreateView,
    SideboardItemCreateJsonView,
    SideboardListPrintView,
)

urlpatterns = [
    path('', SideboardsListView.as_view(), name='sideboards-list'),
    path('create/', SideboardCreateView.as_view(), name='sideboard-create'),
    path('<deck>/', SideboardListView.as_view(), name='sideboard-list'),
    path('<deck>/pdf/', SideboardListPrintView.as_view(), name='sideboard-list-print'),
    path('<slug:slug>/detail/', SideboardDetailView.as_view(), name='sideboard-detail'),
    path('<slug:slug>/edit/', SideboardItemCreateView.as_view(), name='sideboard-edit'),
    path('<slug:slug>/edit-json/', SideboardItemCreateJsonView.as_view(), name='sideboard-edit-json'),
]