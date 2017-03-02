from django.http import HttpResponse
from django.shortcuts import render
from giftshop.models import Category,Item

def index(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}
    return render(request, 'giftshop/index.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        items = Item.objects.filter(category=category)
        context_dict['items'] = items
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['items'] = None
        context_dict['category'] = None
    return render(request, 'giftshop/category.html',context_dict)

def show_item(request, item_name_slug):
    context_dict = {}
    try:
        item = Item.objects.get(slug = item_name_slug)
        context_dict['items'] = item
    except Item.DoesNotExist:
        context_dict['items'] = None
    return render(request, 'giftshop/item.html',context_dict)

def user_login(request):
    return render(request, 'giftshop/login.html', {})

def item_detail(request):
    return render(request, 'giftshop/item.html', {})

def user_register(request):
    return render(request, 'giftshop/register.html', {})
