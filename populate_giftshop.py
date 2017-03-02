import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'UoGgiftshop.settings')

import django
django.setup()
from giftshop.models import Category, Item

def populate():

    clothing_items = [
        {"name": "Clothing 1",
         "url":"http://docs.python.org/2/tutorial/",
         "price": 32,
         "views": 32,
         "description": "This is the clothing one",
         "stock": 1},
        {"name":"Clothing 2",
         "url":"http://www.greenteapress.com/thinkpython/",
         "price": 34.99,
         "views": 21,
         "description": "This is the clothing two",
         "stock": 2},
        {"name":"Clothing 3",
         "url":"http://www.korokithakis.net/tutorials/python/",
         "price": 21.55,
         "views": 37,
         "description": "This is the clothing three",
         "stock": 3}]

    accessories_items = [
        {"name":"Accessories one",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "price": 19.99,
         "views": 126,
         "description": "This is the Accessories one",
         "stock": 3},
        {"name":"Accessories two",
         "url":"http://www.djangorocks.com/",
         "price": 21,
         "views": 475,
         "description": "This is the clothing 2",
         "stock": 74},
        {"name":"Accessories three",
         "url":"http://www.tangowithdjango.com/",
         "price": 32.01,
         "views": 235,
         "description": "This is the clothing 3",
         "stock": 135} ]
    #
    # other_pages = [
    #     {"title":"Bottle",
    #      "url":"http://bottlepy.org/docs/dev/",
    #      "views":32},
    #     {"title":"Flask",
    #      "url":"http://flask.pocoo.org",
    #      "views":16} ]

    cats = {"Clothing": {"items": clothing_items},
            "Accessories": {"items": accessories_items}}

    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for i in cat_data["items"]:
            add_item(c, i["name"], i["url"],i["price"],i["views"],i["description"],i["stock"])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for i in Item.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(i)))


def add_item(cat, name, url, price, views, description, stock):
     i = Item.objects.get_or_create(category=cat, name=name)[0]
     i.url=url
     i.price = price
     i.views=views
     i.description = description
     i.stock = stock
     i.save()
     return i

def add_cat(name):
     c = Category.objects.get_or_create(name=name)[0]
     c.save()
     return c

# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()