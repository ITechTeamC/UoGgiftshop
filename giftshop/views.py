from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context_dict = {'boldmessage': "it should be change to 'categories': category_list, 'item': item_list"}
    return render(request, 'giftshop/index.html', context=context_dict)

def user_login(request):
    return render(request, 'giftshop/login.html', {})

def user_register(request):
    return render(request, 'giftshop/register.html', {})
