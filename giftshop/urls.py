from django.conf.urls import url
from giftshop import views

urlpatterns = [
    url(r'^$', views.index, name= 'index'),
<<<<<<< HEAD
    url(r'^login/$', views.user_login, name= 'login'),
    url(r'^item/$', views.item_detail, name= 'item'),
=======
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.user_register, name='register'),
>>>>>>> origin/master
]
