from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


# conn, cur = DbUtil.getConn()


def getData(name, id, score, totalDownload):
    commentUrl = "http://comment.mobilem.360.cn/comment/getComments?baike=%s&start=%s&count=%s"
    start, count = 0, 50
    result = BsUtil.praseJson(commentUrl % (id, start, 1))
    totalComCount = result['data']['total']

    print('INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
          'VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' % (
              name, '360', totalComCount, score,
              totalDownload, DateUtil.currentDate()))

    while (True):
        result = BsUtil.praseJson(commentUrl % (id, start, count))
        if not result['data']['messages']:
            break
        for comment in result['data']['messages']:
            print(comment['username'], comment['content'], comment['score'], comment['create_time'])
            print('INSERT INTO comment(game_id, content, comment_time, author, score) '
                  'VALUES ("%s", "%s", "%s", "%s", %s);' % (
                      0, comment['content'].replace('\n', ''), comment['create_time'],
                      comment['username'], comment['score']))
        start += 50


def getTop50():
    result = BsUtil.praseGzipJson("http://openbox.mobilem.360.cn/app/rank?from=game&type=download&startCount=1")
    print(result)
    for app in result['data']:
        print(app['name'], app['id'], app['rating'], app['download_times'])
        getData(app['name'], app['id'], app['rating'], app['download_times'])


if __name__ == '__main__':
    getTop50()
