#!/usr/bin/python 
# -*- coding: UTF-8 -*-

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import svm
from sklearn import naive_bayes
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from preprocessing import *
from evaluate import *
import pickle

def decision_tree():
    model = DecisionTreeClassifier()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    print classification_report(Y_test, Y_pred), '(decision_tree)'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)

def log_reg():
    # 训练LR模型，并进行预测
    model = LogisticRegression(penalty='l2')
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    save_model(model, 'lr.txt')
    print classification_report(Y_test, Y_pred), '(logistic regression)'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)

def random_forest():
    model = RandomForestClassifier()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    save_model(model, 'random_forest.txt')
    print classification_report(Y_test, Y_pred), '(random forest)'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)

def gbdt():
    # n_estimators = 90 , min_samples_split=800, max_depth=17, min_samples_leaf=60, subsample=0.9
    # model = GradientBoostingClassifier(random_state=10, n_estimators=90,
    #                                    min_samples_split=800, max_depth=17,
    #                                    min_samples_leaf=60, subsample=0.9)
    model = GradientBoostingClassifier()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    save_model(model, 'gbdt.txt')
    print classification_report(Y_test, Y_pred), '(gdbt)'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)

def gbdt_lr_classifier():
    # 弱分类器数
    n_estimator = 60
    # 将训练集切分为两部分，一部分用于训练GBDT模型，另一部分输入到训练好的GBDT模型生成GBDT特征，
    # 然后作为LR的特征。这样分成两部分是为了防止过拟合。
    x_train, x_train_lr, y_train, y_train_lr = train_test_split(X_train, Y_train, test_size=0.5)
    # 调用GBDT分类模型
    gb = GradientBoostingClassifier(n_estimators=n_estimator)
    # 调用one-hot编码
    onehot = OneHotEncoder()
    # 调用LR分类模型
    lr = LogisticRegression()
    # 使用x_train训练GBDT模型，后面用此模型构造特征
    gb.fit(x_train, y_train)
    # fit one-hot编码器
    onehot.fit(gb.apply(x_train)[:, :, 0])
    # 使用训练好的GBDT模型构建特征，然后将特征经过one-hot编码作为新的特征输入到LR模型训练
    lr.fit(onehot.transform(gb.apply(x_train_lr)[:, :, 0]), y_train_lr)
    Y_pred = lr.predict(onehot.transform(gb.apply(X_test)[:, :, 0]))
    print classification_report(Y_test, Y_pred), 'gbdt-lr'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)

def svm_classifier():
    model = svm.SVC(C=1.0, kernel='rbf', gamma='auto')
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    save_model(model, 'svm.txt')
    print classification_report(Y_test, Y_pred), '(svm)'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)

# naive bayes
def bayes():
    # 文本分类问题常用MultinomialNB
    model = naive_bayes.MultinomialNB(alpha=1.0, fit_prior=True, class_prior=None)
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    save_model(model, 'bayes.txt')
    print classification_report(Y_test, Y_pred), '(naive bayes)'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)

def mlp_classifier():
    model = MLPClassifier()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    save_model(model, 'mlp.txt')
    print classification_report(Y_test, Y_pred), '(mlp)'
    precison_recall_f1(y_true=Y_test, y_pred=Y_pred)


# gbdt调参
def gbdtParameterTest():
    # 迭代次数调参
    # param_test1 = {'n_estimators': range(20, 101, 10)}
    # gsearch = GridSearchCV(estimator=GradientBoostingClassifier(learning_rate=0.1, min_samples_split=300,
    #                                                              min_samples_leaf=20, max_depth=8, max_features='sqrt',
    #                                                              subsample=0.8, random_state=10),
    #                         param_grid=param_test1, scoring='roc_auc', iid=False, cv=5)

    # max_depth,min_samples_split调参
    # param_test2 = {'max_depth': range(3, 21, 2), 'min_samples_split': range(100, 801, 200)}
    # gsearch = GridSearchCV(
    #     estimator=GradientBoostingClassifier(learning_rate=0.1, n_estimators=90, min_samples_leaf=20,
    #                                          max_features='sqrt', subsample=0.8, random_state=10),
    #     param_grid=param_test2, scoring='roc_auc', iid=False, cv=5)

    # min_samples_split, min_samples_leaf调参
    # param_test3 = {'min_samples_split': range(800, 1900, 200), 'min_samples_leaf': range(60, 101, 10)}
    # gsearch = GridSearchCV(
    #     estimator=GradientBoostingClassifier(learning_rate=0.1, n_estimators=90, min_samples_leaf=20,
    #                                          max_features='sqrt', subsample=0.8, random_state=10),
    #     param_grid=param_test3, scoring='roc_auc', iid=False, cv=5)

    # subsample采样比例调参
    # param_test5 = {'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9]}
    # gsearch = GridSearchCV(
    #     estimator=GradientBoostingClassifier(learning_rate=0.1, n_estimators=90, max_depth=17, min_samples_leaf=60,
    #                                          min_samples_split=800, max_features=1000, random_state=10),
    #     param_grid=param_test5, scoring='roc_auc', iid=False, cv=5)
    #
    # gsearch.fit(X_train, Y_train)
    # print gsearch.best_estimator_, gsearch.best_params_, gsearch.best_score_
    pass

def save_model(model, model_name):
    s = pickle.dumps(model)
    f = open('../model/' + model_name, 'w')
    f.write(s)
    f.close()

def read_model(model_name):
    print 'read model', model_name
    f2 = open('../model/' + model_name, 'r')
    s2 = f2.read()
    model = pickle.loads(s2)
    return model


def test():
    # 用于案例测试
    comment = []
    rating = []
    comment.append(u"屏幕够大")
    comment.append(u"手机运行挺流畅")
    comment.append(u"外观看起来还可以")
    comment.append(u"这手机卡的一批")
    comment.append(u"电池发热很厉害")
    comment.append(u"手机打王者荣耀挺爽的")
    comment.append(u"屏幕够大了")
    comment.append(u"屏幕手感很好")
    comment.append(u"拍照真的好a")
    comment.append(u"续航很强")
    rating.append(1)
    rating.append(1)
    rating.append(1)
    rating.append(0)
    rating.append(0)
    rating.append(1)
    rating.append(1)
    rating.append(0)
    rating.append(1)
    rating.append(1)

    for c in parse(comment):
        for w in c:
            print w,
        print '\n'
    x_test, y_test = w2v_feature([parse(text) for text in comment])
    x_test = np.array(x_test)
    y_test = np.array(rating)
    nsamples, nx, ny = x_test.shape
    x_test = x_test.reshape(nsamples, nx*ny)
    model = read_model('mlp.txt')
    y_pred = model.predict(x_test)
    print y_test, y_pred
    precison_recall_f1(y_true=y_test, y_pred=y_pred)

def train():
    # 读取所有文本
    # comments, ratings = loadDataset()
    # comments = parse(comments)
    # feature, label = tfidf_feature(comments, ratings)
    # feature, label = w2v_feature(comments, ratings)   # TODO : 评分处理

    # 只读优缺点
    advantage = []
    disadvantage = []
    adv_raw, dis_raw = loadData.read_db()
    # 切割语句的方法，效果不好
    # for adv in adv_raw:
    #     sents = [sent for sent in cut_sentence(adv) if len(sent) > 0]
    #     for s in sents:
    #         advantage.append(s)
    # for dis in dis_raw:
    #     sents = [sent for sent in cut_sentence(dis) if len(sent) > 0]
    #     for s in sents:
    #         disadvantage.append(s)

    # 不切割语句
    advantage = parse(adv_raw)
    disadvantage = parse(dis_raw)
    adv_feature, adv_label = w2v_feature(advantage, 1)
    dis_feature, dis_label = w2v_feature(disadvantage, 0)
    print 'advantage:', len(adv_feature), 'disadvantage:', len(dis_feature)
    feature = adv_feature + dis_feature
    label = adv_label + dis_label
    print 'feature:', len(feature), 'label:', len(label)
    feature = np.array(feature)
    label = np.array(label)
    nsamples, nx, ny = feature.shape
    feature = feature.reshape(nsamples, nx * ny)
    # 划分数据集合，比例为8:2，随机数种子设置为10，X代表构建的训练样本，Y是标签
    global X_train, X_test, Y_train, Y_test
    X_train, X_test, Y_train, Y_test = train_test_split(feature, label, test_size=0.2, random_state=10)
    # log_reg()
    # gbdt()
    mlp_classifier()

if __name__ == '__main__':
    # train()
    test()