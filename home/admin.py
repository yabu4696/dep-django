from django.contrib import admin

from .models import Item_category
# class ContentImageInline(admin.TabularInline):
#     model = ContentImage
#     extra = 1


# class PostAdmin(admin.ModelAdmin):
#     inlines = [
#         ContentImageInline,
#     ]

admin.site.register(Item_category)
