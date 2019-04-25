from django.urls import path
from .views import SideboardDetailView

urlpatterns = [
    path('<slug:pk>/', SideboardDetailView.as_view(), name='sideboard-detail'),
]