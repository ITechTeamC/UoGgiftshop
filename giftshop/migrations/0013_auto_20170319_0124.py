# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 01:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('giftshop', '0012_auto_20170317_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='itemID',
        ),
        migrations.RemoveField(
            model_name='review',
            name='userID',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]