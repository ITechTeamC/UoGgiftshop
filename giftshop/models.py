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
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Item, self).save( *args, **kwargs)
    def __str__(self):
        return self.name


class Review(models.Model):
    userID = models.OneToOneField(User)
    itemID = models.ForeignKey(Item)
    title = models.CharField(max_length=128)
    rating = models.IntegerField(default=0)
    content = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


class wishlist(models.Model):
    userID = models.OneToOneField(User)
    itemID = models.ForeignKey(Item)
    addedDate = models.DateField()

    def __str__(self):
        return self.itemID


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    address = models.TextField()
    phoneNumber = models.CharField(max_length=16, unique=True)
    dob = models.DateField()

    def __str__(self):
        return self.user.username