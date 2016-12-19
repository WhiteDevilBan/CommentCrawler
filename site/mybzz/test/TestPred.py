from sklearn.externals import joblib

from site.mybzz.test import NltkUtil
from site.mybzz.util import DbUtil
import jieba

stop = []


def getStop():
    f = open("../StopWords.txt", encoding="utf-8")
    jieba.load_userdict("c:/dict.txt")

    while True:
        line = f.readline().replace("\n", '')

        if not line:
            break
        stop.append(line)


def toDict(list):
    return dict([(word, True) for word in list if word in best_words])


def features(feature_extraction_method):
    Features = []
    for i in lists:
        words = feature_extraction_method(i)  # 为积极文本赋予"pos"
        Features.append(words)
    return Features


if __name__ == '__main__':
    getStop()

    comments = list(DbUtil.getAllResult("select * from comment"))

    lists = []
    for comment in comments:
        list = []
        result = jieba.cut(comment[2])
        for word in result:
            if word not in stop and word != ' ':
                list.append(word)

        lists.append(list)

    word_scores = NltkUtil.create_word_bigram_scores()
    best_words = NltkUtil.find_best_words(word_scores, int(500))

    dataset = features(toDict)

    clf = joblib.load('model.m')

    tags = clf.classify_many(dataset)
    count = 0
    conn, cur = DbUtil.getConn()
    for tag in tags:
        if (tag == 'pos'):
            print('UPDATE comment set type = %d where id = %d;' % (1, comments[count][0]))
            cur.execute('UPDATE comment set type = %d where id = %d;' % (1, comments[count][0]))
        else:
            print('UPDATE comment set type = %d where id = %d;' % (2, comments[count][0]))
            cur.execute('UPDATE comment set type = %d where id = %d;' % (2, comments[count][0]))
        count += 1

    conn.commit()
    DbUtil.close(conn,cur)