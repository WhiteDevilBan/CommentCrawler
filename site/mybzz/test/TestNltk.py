import pickle

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from site.mybzz.test import NltkUtil
import matplotlib.pyplot as plt
from sklearn.externals import joblib

pos = pickle.load(open('pos_review.pkl', 'rb'))
neg = pickle.load(open('neg_review.pkl', 'rb'))


def bag_of_words(words):
    return dict([(word, True) for word in words])


def bigram(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)  # 把文本变成双词搭配的形式
    bigrams = bigram_finder.nbest(score_fn, n)  # 使用了卡方统计的方法，选择排名前1000的双词
    return bag_of_words(bigrams)


def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(words + bigrams)  # 所有词和（信息量大的）双词搭配一起作为特征


def pos_features(feature_extraction_method):
    posFeatures = []
    for i in pos:
        posWords = [feature_extraction_method(i), 'pos']  # 为积极文本赋予"pos"
        posFeatures.append(posWords)
    return posFeatures


def neg_features(feature_extraction_method):
    negFeatures = []
    for j in neg:
        negWords = [feature_extraction_method(j), 'neg']  # 为消极文本赋予"neg"
        negFeatures.append(negWords)
    return negFeatures


def score(classifier):
    # classifier = nltk.SklearnClassifier(classifier)  # 在nltk 中使用scikit-learn 的接口
    # classifier.train(train)  # 训练分类器
    classifier = joblib.load('model.m')
    # joblib.dump(classifier,'model.m')
    pred = classifier.classify_many(dev)  # 对开发测试集的数据进行分类，给出预测的标签

    return precision_recall_fscore_support(tag_dev, pred)


def best_word_features(words):
    return dict([(word, True) for word in words if word in best_words])


if __name__ == '__main__':
    dimension = range(200, 700, 50)
    method_list = ['precision', 'recall', 'fscore']
    index = 150
    pos_dict = {}
    pos_pre_list = []
    pos_recall_list = []
    pos_f_list = []

    neg_dict = {}
    neg_pre_list = []
    neg_recall_list = []
    neg_f_list = []
    
    for d in dimension:
        word_scores = NltkUtil.create_word_bigram_scores()
        best_words = NltkUtil.find_best_words(word_scores, int(d))

        posFeatures = pos_features(best_word_features)
        negFeatures = neg_features(best_word_features)

        train = posFeatures[index:] + negFeatures[index:]
        devtest = posFeatures[:index] + negFeatures[:index]
        test = posFeatures[:5] + negFeatures[:5]
        dev, tag_dev = zip(*devtest)

        # print('Feature number %s' % d)
        precision,recall,fscore,support = score(LinearSVC(C=0.1))
        pos_pre_list.append(round(precision[1],3))
        pos_recall_list.append(round(recall[1], 3))
        pos_f_list.append(round(fscore[1], 3))

        neg_pre_list.append(round(precision[0], 3))
        neg_recall_list.append(round(recall[0], 3))
        neg_f_list.append(round(fscore[0], 3))
        # print('SVC accuracy is %5.2f %%' % (score(SVC()) * 100))
        # print('LinearSVC accuracy is %5.2f %%' % (score(LinearSVC()) * 100))
        # print('NuSVC accuracy is %5.2f %%' % (score(NuSVC(nu=0.01)) * 100))
        # print("\n")
    
    pos_dict['precision'] = pos_pre_list
    pos_dict['recall'] = pos_recall_list
    pos_dict['fscore'] = pos_f_list
    
    neg_dict['precision'] = neg_pre_list
    neg_dict['recall'] = neg_recall_list
    neg_dict['fscore'] = neg_f_list
    
    # 画图
    for method in method_list:
        plt.plot(dimension, pos_dict[method], '--^', label=method)
        plt.title('pos svm')
        plt.xlabel('feature num')
        plt.ylabel('score')
        plt.ylim((0.75, 0.95))

    plt.legend(loc='upper right', numpoints=1)
    plt.show()

    for method in method_list:
        plt.plot(dimension, neg_dict[method], '--*', label=method)
        plt.title('neg svm')
        plt.xlabel('feature num')
        plt.ylabel('score')
        plt.ylim((0.75, 0.95))

    plt.legend(loc='upper right', numpoints=1)
    plt.show()
