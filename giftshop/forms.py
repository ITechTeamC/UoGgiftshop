from django import forms
from django.contrib.auth.models import User
from giftshop.models import UserProfile,Comment


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phoneNumber','address','dob')


class CommmentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': '60', 'rows': '6'}))

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Comment
        fields = ('content',)