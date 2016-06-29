import jieba
import jieba.analyse
from site.mybzz.util import DbUtil

# conn, cur = DbUtil.getConn()

if __name__ == '__main__':

    f = open("../StopWords.txt", encoding="utf-8")
    # jieba.load_userdict("c:/out1.txt")
    jieba.add_word('神仙道')
    jieba.add_word('炉石')
    jieba.add_word('代金券')
    jieba.add_word('的一款游戏')
    jieba.add_word('根本玩不')
    # l = []
    # while True:
    #     line = f.readline().replace("\n", '')
    #
    #     if not line:
    #         break
    #     l.append(line)
    result = jieba.cut('希望能看见我的话我的破血头啊啊啊')

    for seg in result:
        print(seg)

    print(",".join(jieba.analyse.extract_tags('希望能看见我的话我的破血头啊啊啊', topK=3)))
    # comments = DbUtil.getAllResult("select * from comment where game_id = 3")
    # for comment in comments:
    #
    #     print(comment[2])
    #     result = jieba.cut(comment[2])
    #     print(len(list(result)))
    #     #
    #     # for seg in result:
    #     #     if seg not in l:
    #     #         print(seg)
    #
    #     print(",".join(jieba.analyse.extract_tags(comment[2], topK=3)))
    #     print('-------------')