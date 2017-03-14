from django import forms
from django.contrib.auth.models import User
from giftshop.models import UserProfile
from giftshop.models import Wishlist

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phoneNumber','address','dob','website', 'picture')


class WishListForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ('user', 'item','addedDate')
