from django.forms import ModelForm
from .models import SideboardItem, Sideboard

class SideboardForm(ModelForm):
    class Meta:
        model = Sideboard
        fields = ['deck', 'opponent', 'owner']


class SideboardItemForm(ModelForm):
    class Meta:
        model = SideboardItem
        fields = ['card', 'delta', 'sideboard']
