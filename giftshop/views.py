from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from giftshop.models import Category,Item, Wishlist
from giftshop.forms import UserForm, UserProfileForm, WishListForm

def get_categories(context_dict):
    category_list = Category.objects.all()
    context_dict['categories'] = category_list
    return context_dict

def index(request):
    # category_list = Category.objects.all()
    # context_dict = {'categories': category_list}

    return render(request, 'giftshop/index.html', get_categories({}))

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
    return render(request, 'giftshop/category.html',get_categories(context_dict))

def show_item(request, item_name_slug):
    context_dict = {}
    try:
        item = Item.objects.get(slug = item_name_slug)
        context_dict['items'] = item
    except Item.DoesNotExist:
        context_dict['items'] = None
    return render(request, 'giftshop/item.html',get_categories(context_dict))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

            return index(request);
            #return render(request, 'giftshop/index.html', context_dict)
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'giftshop/register.html',get_categories(context_dict))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Sorry, your account is disabled. Please try again.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'giftshop/login.html', get_categories({}))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def item_detail(request):
    return render(request, 'giftshop/item.html', {})

def user_register(request):
    return render(request, 'giftshop/register.html', {})

@login_required
def user_wishlist(request, userID):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        items = Item.objects.filter(category=category)
        context_dict['items'] = items
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['items'] = None
        context_dict['category'] = None
    return render(request, 'giftshop/wishlist.html', get_categories(context_dict))
