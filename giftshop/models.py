from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify





class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save( *args, **kwargs)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



class Item(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=128, unique=True)
    price = models.FloatField(default=0)
    description = models.TextField()
    url = models.URLField()
    views = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='profile_images', blank=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Item, self).save( *args, **kwargs)
    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, null=True)
    item = models.ForeignKey(Item, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    rate = models.IntegerField(default=0)
    def __str__(self):
        return self.content


class Wishlist(models.Model):
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)
    added_date = models.DateField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.item.name


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='user')
    address = models.TextField(default = '')
    phoneNumber = models.CharField(max_length=16, default = '')
    dob = models.DateField()
    def __str__(self):
        return self.user.username


class Itempictures(models.Model):
    item = models.ForeignKey(Item)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    def __str__(self):
        return self.item.name
