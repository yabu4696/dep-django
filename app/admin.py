from django.contrib import admin

from app.models import Item_maker, Tag, Wantoitem

# class ContentImageInline(admin.TabularInline):
#     model = ContentImage
#     extra = 1


# class PostAdmin(admin.ModelAdmin):
#     inlines = [
#         ContentImageInline,
#     ]

class WantoitemAdmin(admin.ModelAdmin):
    fields = ('item_name', 'maker_name', 'tag', 'created_at', 'updated_at', 'slug')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Item_maker)
admin.site.register(Tag)
admin.site.register(Wantoitem, WantoitemAdmin)
