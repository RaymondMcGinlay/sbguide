from django.contrib import admin
from .models import Sideboard, SideboardItem

class SideboardItemInline(admin.TabularInline):
    model = SideboardItem
    raw_id_fields = ('card',)

class SideboardAdmin(admin.ModelAdmin):
    inlines = [SideboardItemInline,]

admin.site.register(Sideboard, SideboardAdmin)
