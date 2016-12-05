import multiprocessing

from gensim.models import word2vec
import jieba
from gensim.models.word2vec import LineSentence
from site.mybzz.util import DbUtil

stop = []

def train(fileName, modelName):
    model = word2vec.Word2Vec(['a','b','c'],size=200,window=5,min_count=5,workers=multiprocessing.cpu_count())
    model.save(modelName)
    return model


def cut():
    comments = DbUtil.getAllResult("select * from comment limit 300000")


    file = open("test1.txt", "w",encoding="utf-8")
    for comment in comments:
        list = []
        result = jieba.cut(comment[2])
        for word in result:
            if word not in stop and word != ' ':
                list.append(word)

        if list:
            file.write(" ".join(list))
            file.write("\n")
    file.close()
    pass

def getStop():
    
    f = open("../StopWords.txt", encoding="utf-8")
    jieba.load_userdict("c:/dict.txt")

    while True:
        line = f.readline().replace("\n", '')

        if not line:
            break
        stop.append(line)
    

if __name__ == '__main__':

    getStop()

    cut()

    # model = train("test.txt","model")
    #
    # for w in model.most_similar(u'魅族'):
    #     print(w[0], w[1])
