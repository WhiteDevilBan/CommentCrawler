import random
from operator import itemgetter
import jieba
import jieba.analyse
from pytagcloud import make_tags, create_tag_image
from pytagcloud.colors import COLOR_SCHEMES
from site.mybzz.util import DbUtil

stop = []

def plot(game_name, game_id):
    dict = {}
    comments = DbUtil.getAllResult("select * from comment where game_id = %s" % game_id)
    for comment in comments:

        result = jieba.analyse.extract_tags(comment[2], topK=3)

        for word in result:
            if len(word) < 2:
                continue
            elif word in stop:
                continue

            if word not in dict:
                dict[word] = 1
            else:
                dict[word] += 1

    print(dict)

    swd = sorted(dict.items(), key=itemgetter(1), reverse=True)
    swd = swd[1:50]
    tags = make_tags(swd,
                     minsize=30,
                     maxsize=120,
                     colors=random.choice(list(COLOR_SCHEMES.values())))

    create_tag_image(tags,
                     'c:/%s.png' % game_name,
                     background=(0, 0, 0, 255),
                     size=(900, 600),
                     fontname='SimHei')

    print('having save file to dick')


if __name__ == '__main__':

    f = open("../StopWords.txt", encoding="utf-8")
    jieba.load_userdict("c:/dict.txt")

    while True:
        line = f.readline().replace("\n", '')

        if not line:
            break
        stop.append(line)

    games = DbUtil.getAllResult("select game_id,games.game_name from `comment` join games on game_id = games.id GROUP BY game_id ORDER BY count(game_id) desc limit 50")

    l =[]
    for game in games:
        if game[1] not in l:
            plot(game[1], game[0])
            l.append(game[1])
