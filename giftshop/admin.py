from django.contrib import admin
from giftshop.models import Category, Item

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)

