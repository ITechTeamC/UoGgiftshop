from django.conf.urls import url
from giftshop import views

urlpatterns = [
    url(r'^$', views.index, name= 'index'),
]
