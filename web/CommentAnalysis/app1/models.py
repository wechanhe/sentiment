# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Sentiment(models.Model):
    name = models.CharField(max_length=20, null=False)
    brand = models.CharField(max_length=50, null=False)
    aspect = models.CharField(max_length=10, null=False)
    comments = models.IntegerField(null=False)
    positive = models.IntegerField(null=False)
    negative = models.IntegerField(null=False)
    pos_list = models.CharField(max_length=100, null=True)  # 存储正向评论ID
    neg_list = models.CharField(max_length=100, null=True)  # 存储负向评论ID

class Result(models.Model):
    name = models.CharField(max_length=20, null=False)
    brand = models.CharField(max_length=50, null=False)
    aspect = models.CharField(max_length=10, null=False)
    comments = models.IntegerField(null=False)
    positive = models.IntegerField(null=False)
    negative = models.IntegerField(null=False)
    pos_list = models.CharField(max_length=100, null=True)  # 存储正向评论ID
    neg_list = models.CharField(max_length=100, null=True)  # 存储负向评论ID