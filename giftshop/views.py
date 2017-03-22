from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from giftshop.models import Category,Item, Wishlist, Comment,UserProfile,Itempictures
from giftshop.forms import UserForm, UserProfileForm, CommmentForm
from django.shortcuts import redirect
from urlparse import urljoin
import urlparse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from datetime import datetime

def get_categories(context_dict):
    category_list = Category.objects.all()
    context_dict['categories'] = category_list
    return context_dict

def index(request):
    # category_list = Category.objects.all()
    # context_dict = {'categories': category_list}
    context_dict ={}
    item_list = Item.objects.order_by('-views')[:6]
    context_dict['items'] = item_list
    return render(request, 'giftshop/index.html', get_categories(context_dict))

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
        return redirect('/giftshop/wishlist/')

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
        rate = form.cleaned_data['rate']
        c = Comment(content=new_comment, item = getItem, rate = rate)  # have tested by shell
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

            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']

            profile.save()
            registered = True

            return index(request);
            #return render(request, 'giftshop/index.html', context_dict)
        else:
            error_profile_msg = profile_form.errors
            error_user_msg = user_form.errors
            context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'error_user_msg':error_user_msg, 'error_profile_msg':error_profile_msg}
            return render(request, 'giftshop/register.html',get_categories(context_dict))
            #print(user_form.errors, profile_form.errors)
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
                error_msg = "Sorry, your account is disabled. Please try again."
                context_dict = {'error_msg': error_msg}
                return render(request, 'giftshop/login.html', get_categories(context_dict))
        else:
            error_msg = "Invalid login details - check UserName:{0} and  Password".format(username)
            context_dict = {'error_msg': error_msg}
            return render(request, 'giftshop/login.html', get_categories(context_dict))
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
def register_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return index(request)
        else:
            print  form.errors
    else:
        form = UserProfileForm()
    return render(request, 'giftshop/profile.html',{'form':form})

@login_required
def profile_page(request, username):
    user = get_object_or_404(User, username=username)
    return render (request, 'giftshop/profile.html',{'profile_user':user})

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'phoneNumber': userprofile.phoneNumber, 'address': userprofile.address, 'dob': userprofile.dob})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile',user.username)
        else:
            print(form.errors)
    return render(request, 'giftshop/profile.html',
                  {'userprofile': userprofile,'selecteduser': user, 'form':form})

def user_setting(request):
	return render(request, 'giftshop/setting.html', get_categories({}))



def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)

    if not val:
        val = default_val
    return val


# Updated the function definition
def visitor_cookie_handler(request,item):
    visits = int(item.views)

    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds >1:
        visits = visits + 1
        item.views = visits
        item.save(update_fields=['views'])
        # update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # Update/set the visits cookie
    request.session['visits'] = visits
	


def show_item(request, item_name_slug):
    context_dict = {}
    commentform = CommmentForm()
    try:
        item = Item.objects.get(slug = item_name_slug)
        comments = Comment.objects.filter(item=item)
        totalrate = 0.0
        i = comments.count()
        if i == 0:
            i = 1
        for n in comments:
            totalrate += float(n.rate)
        totalrate = totalrate / i
        pictures = Itempictures.objects.filter(item=item)
        context_dict['items'] = item
        context_dict['comments'] = comments
        context_dict['category'] = item.category
        context_dict['pictures'] = pictures
        context_dict['commentform'] = commentform
        context_dict['totalrate'] = totalrate
    except Item.DoesNotExist:
        context_dict['items'] = None
        context_dict['comments'] = None
        context_dict['category'] = None
        context_dict['pictures'] = None
    response = render(request, 'giftshop/item.html',get_categories(context_dict))

    visitor_cookie_handler(request, item)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'giftshop/item.html', get_categories(context_dict))
    return response