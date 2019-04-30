from django.conf.urls import url
from .views import CardAutocomplete

urlpatterns = [
    url(
        r'^card-autocomplete/$',
        CardAutocomplete.as_view(),
        name='card-autocomplete',
    ),
]