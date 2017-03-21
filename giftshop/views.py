from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from giftshop.models import Category,Item, Wishlist, Comment,UserProfile
from giftshop.forms import UserForm, UserProfileForm, CommmentForm
from django.shortcuts import redirect
from urlparse import urljoin
import urlparse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    commentform = CommmentForm()
    try:
        item = Item.objects.get(slug = item_name_slug)
        comments = Comment.objects.filter(item=item)
        context_dict['items'] = item
        context_dict['comments'] = comments
        context_dict['category'] = item.category
        context_dict['commentform'] = commentform
    except Item.DoesNotExist:
        context_dict['items'] = None
        context_dict['comments'] = None
    return render(request, 'giftshop/item.html',get_categories(context_dict))

@login_required
def my_comments(request):
    context_dict = {}
    try:
        user = request.user
#        comments = user.comment_set.all()
        comments = Comment.objects.filter(user=user)
        context_dict['comments'] = comments
    except Comment.DoesNotExist:
        context_dict['comments'] = None
    return render(request, 'giftshop/mycomments.html',get_categories(context_dict))


@login_required
def add_wishlist(request, item_name_slug):
    b = False
    user = request.user
    item = Item.objects.get(slug=item_name_slug)
    wishlist = Wishlist.objects.filter(user=user)
    for items in wishlist:
        if item == items.item:
            b = True
    if b == False:
        wl = Wishlist(user=user, item=item)
        wl.save()
        return redirect('/giftshop/wishlist/')
    else:
        return redirect('/giftshop/')

@login_required
def delete_wishlist(request, item_name_slug):
    user = request.user
    item = Item.objects.get(slug=item_name_slug)
    wishlist = Wishlist.objects.filter(user=user,item = item)
    wishlist.delete()
    return redirect('/giftshop/wishlist/')


@login_required
def add_comment(request,category_name_slug,item_name_slug):
    try:
        getItem = Item.objects.get(slug=item_name_slug)
    except Item.DoesNotExist:
        getItem = None
    form = CommmentForm(request.POST)
    url = urlparse.urljoin('/giftshop/category/',category_name_slug+'/'+item_name_slug)

    if form.is_valid():
        user = request.user
        new_comment = form.cleaned_data['comment']
        c = Comment(content=new_comment, item = getItem)  # have tested by shell
        c.user = user
        c.save()
        #article.comment_num += 1
    return redirect(url)

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
#def user_wishlist(request):
#    context_dict = {}
#    try:
#        user = request.user
        #        comments = user.comment_set.all()
#        wishlists = Wishlist.objects.filter(user=user)
#        context_dict['wishlists'] = wishlists
#    except Comment.DoesNotExist:
#        context_dict['wishlists'] = None
#    return render(request, 'giftshop/wishlist.html', get_categories(context_dict))
	
	
def user_wishlist(request):
    user = request.user
    wish_list = Wishlist.objects.filter(user=user)
    paginator = Paginator(wish_list, 5) # Show 3 contacts per page
    page = request.GET.get('page')
    try:
        wishlists = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        wishlists = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        wishlists = paginator.page(paginator.num_pages)

    return render(request, 'giftshop/wishlist.html', {'wishlists': wishlists})

@login_required
def user_profile(request):
   
	return render(request, 'giftshop/profile.html')

def user_setting(request):
	return render(request, 'giftshop/setting.html', get_categories({}))
