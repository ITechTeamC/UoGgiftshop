from django.contrib import admin
from giftshop.models import Category, Item, UserProfile, Comment,Wishlist


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user_id','item_id','added_date')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id','item_id','pub_date', 'content')

admin.site.register(Comment,CommentAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(UserProfile)
