#!/usr/bin/python 
# -*- coding: UTF-8 -*-

import jieba.analyse
from model import *
from preprocessing import *
from util import *

w2v_path = '/local/w2v.model'
w2v_model = Word2Vec.load(w2v_path)
dictionary = []

def load_dictionary():
    '''
    加载字典
    :return:
    '''
    global dictionary
    with open('/local/TextClassification/dictionary.txt', 'r') as file:
        for line in file.readlines():
            dictionary.append(line.strip('\n'))

def get_aspect(comment = ''):
    '''
    评论对象抽取
    :return:
    '''
    keywords = jieba.analyse.extract_tags(comment, topK=1000,
                                          allowPOS=('n', 'ns', 'nl', 'nz', 'vn', 'an', 'v'))
    aspect = set()
    for word in keywords:
        max = 0.0
        label = ''
        for d_word in dictionary:
            try:
                sim = w2v_model.similarity(d_word, word.encode('utf-8'))
                if sim > max and sim > 0.5:
                    max = sim
                    label = d_word
            except:
                pass
        if label != '':
            aspect.add(label)
    return aspect

def sentiment_analyse(comment = ''):
    new_comment = parse([comment])
    x_test, y_test = w2v_feature(new_comment)
    x_test = np.array(x_test)
    # y_test = np.array(rating)
    nsamples, nx, ny = x_test.shape
    x_test = x_test.reshape(nsamples, nx * ny)
    model = read_model('lr_2.txt')
    y_pred = model.predict(x_test)
    # print y_test, y_pred
    # precison_recall_f1(y_true=y_test, y_pred=y_pred)
    return y_pred[0]

def extraction():
    '''
    导入所有
    :return:
    '''
    rawdata = loadData.read_rawdata()
    res = {}
    count = 0
    for data in rawdata:
        print 'processing record ', count
        count += 1
        name = data[0]
        brand = data[1]
        advantage = data[2]
        disadvantage = data[3]
        if advantage != '':
            sentences = cut_sentence(advantage)   # 评论分句
            for sent in sentences:
                for asp in get_aspect(sent):   # 抽取分句的评论对象
                    key = (name, brand, asp)
                    value = res.get(key)
                    if value is not None:
                        res[key] = [value[0]+1, value[1]+1, value[2]]
                    else:
                        res.setdefault(key, [1, 1, 0])
        if disadvantage != '':
            sentences = cut_sentence(disadvantage)   # 评论分句
            for sent in sentences:
                for asp in get_aspect(sent):   # 抽取分句的评论对象
                    key = (name, brand, asp)
                    value = res.get(key)
                    if value is not None:
                        res[key] = [value[0] + 1, value[1], value[2]+1]
                    else:
                        res.setdefault(key, [1, 0, 1])
    count = 0
    with open('/local/TextClassification/sentiment.txt', 'w') as file:
        file.write(str(len(res)) + '\n')
        for key in res.keys():
            name = key[0]
            brand = key[1]
            asp = key[2]
            value = res.get(key)
            total = value[0]
            pos = value[1]
            neg = value[2]
            record = (name, brand, asp, total, pos, neg, '', '')
            for i in range(len(record)):
                file.write(str(record[i])+',')
            file.write('\n')
            print 'succeed to add', count
            count += 1

def test():
    comment = '屏幕够大,外观看起来还可以'
    sents = cut_sentence(comment)
    for sent in sents:
        sentiment = sentiment_analyse(sent)   # 对每一个分句进行情感分析
        for asp in get_aspect(sent):   # 抽取分句的评论对象
            print asp, sentiment
        print '\n'

def text2db():
    count = 0
    with open('/local/TextClassification/sentiment.txt', 'r') as file:
        for line in file.readlines():
            record = line.split(',')
            record[3] = int(record[3])
            record[4] = int(record[4])
            record[5] = int(record[5])
            if add(record) == True:
                print 'succeed to add', count
            else:
                print 'fail to add', count
            count += 1

if __name__ == '__main__':
    # load_dictionary()
    # extraction()
    # text2db()
    pass