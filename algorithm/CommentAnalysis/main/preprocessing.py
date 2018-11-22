#!/usr/bin/python 
# -*- coding: UTF-8 -*-

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from gensim.models import Word2Vec
import loadData
import jieba
import jieba.analyse
import numpy as np
import codecs
import re

w2v_path = '/local/w2v.model'
print 'loading word2vec...'
model = Word2Vec.load(w2v_path)
print 'load word2vec finished.'

# 加载原始文本
def loadDataset():
    comments, ratings = loadData.getDataset()
    print '样本数:', len(comments)
    return comments, ratings

# 加载停用词
def loadStopWords():
    path = '/local/TextClassification/stopwords.txt'
    stopwords = set()
    with codecs.open(path, mode='r', encoding='utf8') as file:
        # stopwords = set(w.strip() for w in file.readlines())
        for line in file.readlines():
            stopwords.add(line.strip().encode('utf8'))
    return stopwords

def cut_sentence(comment = ''):
    '''
    分句
    :param comment:
    :return:
    '''
    sents = re.split('\,|\，|\.|\。|\!|\！|\？|\?|\、|\:|\：|\d+', comment)
    # sents = re.split('，', comment)
    return sents

# 分词，去停用词
# input: rawdata--datatype={}
# output: list[list] , list[int]
def parse(comments):
    new_comments = []
    stopwords = loadStopWords()
    for text in comments:
        words = [word.encode('utf-8') for word in jieba.cut(text, cut_all=False)]
        tmp = []
        for word in words:
            if word not in stopwords:
                tmp.append(word)
        if len(tmp) > 0:
            new_comments.append(tmp)
    return new_comments

# 特针工程
# 使用TF-IDF生成评论的向量，标签二分类：评分大于5为正样本，否则为负样本
def tfidf_feature(comments = [], ratings = []):
    feature_matrix = []
    rating_vector = []
    corpus = []
    counter = 0
    for comment in comments:
        c = ''
        for word in comment:
            c += ' ' + word
        corpus.append(c)
    vectorizer = CountVectorizer(ngram_range=(1, 1))
    transformer = TfidfTransformer()
    feature_matrix = transformer.fit_transform(vectorizer.fit_transform(corpus))
    print '特征矩阵维度：', feature_matrix.shape[0], feature_matrix.shape[1]
    for rating in ratings:
        if float(rating) > 5.0:
            rating_vector.append(1)
        else:
            counter += 1
            rating_vector.append(0)
    print '正负样本比例：', (len(ratings)-counter)/counter*1.0, ':', 1
    return feature_matrix, rating_vector


def w2v_feature(comments=[], rating = 0):
    '''
    利用word2vec模型提取文本特征, word2vec词向量维度为100
    :param comments: 文本
    :param ratings: 评分
    :return:
    '''
    feature_matrix = []
    rating_vector = []
    for comment in comments:
        vec = np.zeros([1, 100])
        for word in comment:
            try:
                wv = model.wv[word]
                vec += wv
            except:
                pass
        feature_matrix.append(vec)
        rating_vector.append(rating)
    return feature_matrix, rating_vector

def training_w2v(comments):
    '''
    word2vec模型训练
    :param comments:
    :return:
    '''
    sentences = parse(comments)
    model = Word2Vec(sentences=sentences, sg=1)
    model.save(w2v_path)

