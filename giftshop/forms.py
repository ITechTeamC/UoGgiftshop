from django import forms
from django.contrib.auth.models import User
from giftshop.models import UserProfile,Comment,Wishlist

# Password form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# Form to get extra info of users
class UserProfileForm(forms.ModelForm):
    phoneNumber = forms.CharField(required=False)
    address = forms.CharField(required=False)
    dob = forms.DateField(required=False)
    class Meta:
        model = UserProfile
        exclude = ('user',)


# Form to get comments and rate 
class CommmentForm(forms.Form):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'cols': '126', 'rows': '5'}))
    rate = forms.IntegerField(initial=10, required=True, min_value=1,max_value=10)
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Comment
        fields = ('content','rate')
