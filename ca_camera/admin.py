from django.contrib import admin

from .models import Item_maker, Tag, Wantoitem

class WantoitemAdmin(admin.ModelAdmin):
    fields = ('item_name', 'maker_name', 'tag', 'created_at', 'updated_at', 'slug')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Item_maker)
admin.site.register(Tag)
admin.site.register(Wantoitem, WantoitemAdmin)