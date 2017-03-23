from django.conf.urls import url
from giftshop import views

urlpatterns = [
    url(r'^$', views.index, name= 'index'),
    url(r'^login/$', views.user_login, name= 'login'),
    url(r'^item/$', views.item_detail, name= 'item'),
    url(r'^wishlist/$', views.user_wishlist, name='wishlist'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<item_name_slug>[\w\-]+)/add_comment/$',
        views.add_comment, name='add_comment'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<item_name_slug>[\w\-]+)/add_comment/$',views.add_comment, name='add_comment'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^category/([\w\-]+)/(?P<item_name_slug>[\w\-]+)/$', views.show_item, name='show_item'),
    url(r'^category/([\w\-]+)/(?P<item_name_slug>[\w\-]+)/add_wishlist/$', views.add_wishlist, name='add_wishlist'),
    url(r'^wishlist/(?P<item_name_slug>[\w\-]+)/delete_wishlist/$', views.delete_wishlist, name='delete_wishlist'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
	url(r'setting/$', views.user_setting, name='setting'),
	url(r'^mycomments/$',views.my_comments,name='my_comments'),
    url(r'^register_profile/$', views.register_profile, name='register_profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
]
