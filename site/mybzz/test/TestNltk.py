import pickle

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC, LinearSVC, NuSVC

from site.mybzz.test import NltkUtil

pos = pickle.load(open('pos_review.pkl', 'r'))
neg = pickle.load(open('neg_review.pkl', 'r'))

def bag_of_words(words):
    return dict([(word, True) for word in words])


def bigram(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)  #把文本变成双词搭配的形式
    bigrams = bigram_finder.nbest(score_fn, n) #使用了卡方统计的方法，选择排名前1000的双词
    return bag_of_words(bigrams)

def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(words + bigrams)  #所有词和（信息量大的）双词搭配一起作为特征


def pos_features(feature_extraction_method):
    posFeatures = []
    for i in pos:
        posWords = [feature_extraction_method(i),'pos'] #为积极文本赋予"pos"
        posFeatures.append(posWords)
    return posFeatures

def neg_features(feature_extraction_method):
    negFeatures = []
    for j in neg:
        negWords = [feature_extraction_method(j),'neg'] #为消极文本赋予"neg"
        negFeatures.append(negWords)
    return negFeatures


def score(classifier):
    classifier = nltk.SklearnClassifier(classifier) #在nltk 中使用scikit-learn 的接口
    classifier.train(train) #训练分类器

    pred = classifier.batch_classify(devtest) #对开发测试集的数据进行分类，给出预测的标签
    return accuracy_score(tag_dev, pred) #对比分类预测结果和人工标注的正确结果，给出分类器准确度

def best_word_features(words):
    return dict([(word, True) for word in words if word in best_words])

if __name__ == '__main__':
    dimension = ['500', '1000', '1500', '2000', '2500', '3000']

    for d in dimension:
        word_scores = NltkUtil.create_word_bigram_scores()
        best_words = NltkUtil.find_best_words(word_scores, int(d))

        posFeatures = pos_features(best_word_features)
        negFeatures = neg_features(best_word_features)

        train = posFeatures[174:] + negFeatures[174:]
        devtest = posFeatures[124:174] + negFeatures[124:174]
        test = posFeatures[:124] + negFeatures[:124]
        dev, tag_dev = zip(*devtest)

        print
        'Feature number %f' % d
        print
        'SVC`s accuracy is %f' % score(SVC())
        print
        'LinearSVC`s accuracy is %f' % score(LinearSVC())
        print
        'NuSVC`s accuracy is %f' % score(NuSVC())