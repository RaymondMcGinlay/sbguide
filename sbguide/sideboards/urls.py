from django.urls import path
from .views import (
    SideboardDetailView,
    SideboardListView,
    SideboardCreateView,
    SideboardItemCreateView
)

urlpatterns = [
    path('create/', SideboardCreateView.as_view(), name='sideboard-create'),
    path('<deck>/', SideboardListView.as_view(), name='sideboard-list'),
    path('g/<slug:slug>/', SideboardDetailView.as_view(), name='sideboard-detail'),
    path('g/<slug:slug>/edit/', SideboardItemCreateView.as_view(), name='sideboard-edit'),
]