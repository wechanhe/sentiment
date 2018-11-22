#!/usr/bin/python 
# -*- coding: UTF-8 -*-

from django.conf.urls import url
from app1.views import *

urlpatterns = [
    url('^index$', index),
    url('^add$', add_data),
    url('^get$', get_data),
    url('^wordcloud$', wordcloud),
    url('^getbar', getbar),
]
