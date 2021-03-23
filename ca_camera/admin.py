from django.contrib import admin

from .models import Item_maker, Tag, Wantoitem

admin.site.register(Item_maker)
admin.site.register(Tag)
admin.site.register(Wantoitem)