# !/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
import json
from django.shortcuts import render
from models import Sentiment, Result
from django.http import HttpRequest, HttpResponse

# Create your views here.

def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def getbar(request):
    name = 'OPPO R11（标准版/全网通）'
    records = Result.objects.filter(name=name)
    records = sorted(records, key=lambda x: x.comments, reverse=True)
    aspects = []
    pos = []
    neg = []
    for i in range(len(records)):
        if i < 10:
            print records[i].aspect, records[i].positive, records[i].negative
            aspects.append(records[i].aspect)
            pos.append(records[i].positive)
            neg.append(records[i].negative)
    return render(request, 'wordcloud.html', {'aspects': aspects, 'pos': pos, 'neg': neg})

def wordcloud(request):
    pass


def add_data(request):
    s = Sentiment(mobile='tcl', brand='123', aspect='屏幕', comments=1000,
                  positive=800, negative=200, pos_list='1,2,3,4,5', neg_list='6,7,8')
    try:
        s.save()
    except:
        print 'data save failed.'
        return HttpResponse("<p>数据添加失败！</p>")
    return HttpResponse("<p>数据添加成功！</p>")

def get_data(request):
    records = Sentiment.objects.all()
    name = ''
    for record in records:
        name += record.mobile
    print name
    return HttpResponse('<p>' + name + '</p>')
    try:
        pass
    except:
        return HttpResponse('<p>get data failed.</p>')
