from django.contrib import admin
from .models import Card
from django.utils.html import format_html
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="122px" height="170px"  />'.format(obj.image_link))

    image_tag.short_description = 'Image'

    list_display = ['image_tag',]

    list_display = ('name', 'image_tag', 'set_code', 'modern_legal', 'standard_legal')
    list_display_links = ('name', 'image_tag')
    search_fields = ('name',)
    list_filter = ('modern_legal', 'standard_legal')

    readonly_fields = ['image_tag']



admin.site.register(Card, CardAdmin)
