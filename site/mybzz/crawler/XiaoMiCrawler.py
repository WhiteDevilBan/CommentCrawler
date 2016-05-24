import sys

from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


def getTop30():
    page = 0
    result = BsUtil.praseJson(
        'http://market.xiaomi.com/apm/toplist/15?clientId=2bb48bb54747e03a6ab667ab7b51050a&co=CN&la=zh&os=1461822601&page=%d&sdk=22&stamp=0' % page)
    # print(result)
    for game in result['listApp'][28:]:
        print('游戏名：%s，id：%s，总评分：%s' % (game['displayName'], game['id'], game['ratingScore']))
        try:
            getData(game['id'], game['displayName'], game['ratingScore'])
        except:
            print(sys.exc_info()[0], ":", sys.exc_info()[1])
            pass


def getData(id, name, totalScore):
    page = 0
    hasMore = True

    # 插入游戏
    conn, cur = DbUtil.getConn()

    result = BsUtil.praseJson('http://market.xiaomi.com/apm/comment/list/%s?'
                              'clientId=2bb48bb54747e03a6ab667ab7b51050a&co=CN'
                              '&la=zh&os=1461822601&page=%s&sdk=22' % (id, page))
    totalComCount = result['pointCount']

    print('INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
          'VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' % (
              name, 'xiaomi', totalComCount, totalScore * 10, 0, DateUtil.currentDate()))
    cur.execute('INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
                'VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' % (
                    name, 'xiaomi', totalComCount, totalScore * 10, 0, DateUtil.currentDate()))
    game_id = cur.lastrowid
    # game_id = 0
    while (hasMore):
        result = BsUtil.praseJson('http://market.xiaomi.com/apm/comment/list/%s?'
                                  'clientId=2bb48bb54747e03a6ab667ab7b51050a&co=CN'
                                  '&la=zh&os=1461822601&page=%s&sdk=22' % (id, page))
        # print(result)
        for comment in result['comments']:
            content = comment['commentValue'].replace("\"", "'").replace(" ", "")
            score = comment['pointValue']
            time = comment['updateTime']
            author = comment['nickname'].replace("\"", "'")
            # 插入评论
            try:
                print('INSERT INTO comment(game_id, content, comment_time, author, score) '
                      'VALUES ("%s", "%s", "%s", "%s", %d);' % (
                          game_id, content, DateUtil.lomgToStrTime(time / 1000), author, score))
                cur.execute('INSERT INTO comment(game_id, content, comment_time, author, score) '
                            'VALUES ("%s", "%s", "%s", "%s", %d);' % (
                                game_id, content, DateUtil.lomgToStrTime(time / 1000), author, score))
            except:
                print(sys.exc_info()[0], ":", sys.exc_info()[1])
                pass
        page += 1
        hasMore = result['hasMore']

    conn.commit()
    DbUtil.close(conn, cur)


if __name__ == '__main__':
    getTop30()
