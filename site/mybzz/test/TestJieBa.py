import jieba
import jieba.analyse
from site.mybzz.util import DbUtil

conn, cur = DbUtil.getConn()

if __name__ == '__main__':

    f = open("../StopWords.txt", encoding="utf-8")
    l = []
    while True:
        line = f.readline().replace("\n", '')

        if not line:
            break
        l.append(line)

    comments = DbUtil.getAllResult("select * from comment limit 100 offset 383721")
    for comment in comments:

        print(comment)
        result = jieba.cut(comment[2])

        for seg in result:
            if seg not in l:
                print(seg)

        print(",".join(jieba.analyse.extract_tags(comment[2], topK=20)))