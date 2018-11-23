#!/usr/bin/python 
# -*- coding: UTF-8 -*-

from pyecharts import WordCloud
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyecharts import Bar
bar = Bar("我的第一个图表", "这里是副标题")
bar.add("服装", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90],is_more_utils=True)
bar.show_config()
bar.render()

class Visualizaion:
    def __init__(self):
        pass

    def wordcloud():
        wc = WordCloud("绘制词云", width=1000, height=620)
        name = ['Sam S Club', 'Macys', 'Amy Schumer', 'Jurassic World', 'Charter Communications',
                'Chick Fil A', 'Planet Fitness', 'Pitch Perfect', 'Express', 'Home', 'Johnny Depp',
                'Lena Dunham', 'Lewis Hamilton', 'KXAN', 'Mary Ellen Mark', 'Farrah Abraham',
                'Rita Ora', 'Serena Williams', 'NCAA baseball tournament', 'Point Break']

        value = [10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112, 965, 847, 582, 555, 550, 462, 366, 360, 282, 273,
                 265]

        wc.add("", name, value, word_size_range=[20, 100], shape='circle')
