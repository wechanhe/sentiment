#!/usr/bin/python 
# -*- coding: UTF-8 -*-

import tensorflow as tf
from preprocessing import *
from sklearn.model_selection import train_test_split

class TextRNN:
    def __init__(self):
        pass

    def rep_sentencevector(self, sentence):
        '''
        生成句向量
        :return:
        '''
        word_list = parse(sentence)
        max_words = 20
        embedding_dim = 100
        embedding_matrix = np.zeros((max_words, embedding_dim))
        model = Word2Vec.load(w2v_path)
        for index, word in enumerate(word_list):
            try:
                embedding_matrix[index] = model[word]
            except:
                pass
        return embedding_matrix

    def build_traindata():
        '''
        训练集测试集构造
        :return:
        '''
        feature = list()
        label = list()

        comments, ratings = loadDataset()

        for comment in comments:
            sent_vector = rep_sentencevector(comment)
            feature.append(sent_vector)

        for rating in ratings:
            if rating > 5:
                label.append(1)
            else:
                label.append(0)

        X_train, X_test, Y_train, Y_test = train_test_split(feature, label,
                                                            test_size=0.2, random_state=10)
        return np.array(X_train), np.array(Y_train), np.array(X_test), np.array(Y_test)

    def train(self):
        pass

if __name__ == '__main__':
    comments, ratings = loadDataset()
    rnn = TextRNN()
    print len(comments[10])
    for row in rnn.rep_sentencevector(comments[10]):
        print row
