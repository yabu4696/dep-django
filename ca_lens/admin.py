from django.contrib import admin

from .models import Item_maker, Tag, Wantoitem
from adminsortable.admin import SortableAdmin


class Item_makerAdmin(SortableAdmin):
    list_display = ('name',)
    list_display_links = ('name',)

class WantoitemAdmin(SortableAdmin):
    list_display = ('item_name','maker_name')
    list_display_links = ('item_name',)

admin.site.register(Item_maker, Item_makerAdmin)
admin.site.register(Tag)
# admin.site.register(Wantoitem)
admin.site.register(Wantoitem, WantoitemAdmin)