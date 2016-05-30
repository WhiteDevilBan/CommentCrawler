import sys

from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil

conn, cur = DbUtil.getConn()


def getData(name, downloadCount, score, packageName):
    contextData = ''
    url = "http://sj.qq.com/myapp/app/comment.htm?apkName=%s&contextData=%s"

    totalComCount = 0
    while totalComCount == 0:
        try:
            result = BsUtil.praseJson(url % (packageName, contextData))
            totalComCount = result['obj']['total']
        except:
            pass

    print(
        'INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
        'VALUES ("%s", "%s", "%s", %d, "%s", "%s");' % (
            name, 'qq', totalComCount, score, downloadCount, DateUtil.currentDate()))
    cur.execute('INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
                'VALUES ("%s", "%s", "%s", %d, "%s", "%s");' % (
                    name, 'qq', totalComCount, score, downloadCount, DateUtil.currentDate()))
    game_id = cur.lastrowid
    while (True):
        try:
            result = BsUtil.praseJson(url % (packageName, contextData))
            if not result['success']:
                continue
            if result['obj']['hasNext'] != 1:
                break

            contextData = result['obj']['contextData']

            for comment in result['obj']['commentDetails']:
                print('INSERT INTO comment(game_id, content, comment_time, author, score) '
                      'VALUES ("%s", "%s", "%s", "%s", %d);' % (
                          game_id, comment['content'].replace('\r', '').replace(' ', ''),
                          DateUtil.longToStrTime(int(comment['createdTime'])),
                          comment['nickName'], int(comment['score']) * 10))
                cur.execute('INSERT INTO comment(game_id, content, comment_time, author, score) '
                            'VALUES ("%s", "%s", "%s", "%s", %s);' % (
                                game_id, comment['content'].replace('\r', '').replace(" ", ""),
                                DateUtil.longToStrTime(int(comment['createdTime'])),
                                comment['nickName'], int(comment['score']) * 10))
        except:
            conn.commit()
            print(result)
            print(sys.exc_info()[0], ":", sys.exc_info()[1])


def getTop():
    url = "http://pngweb.3g.qq.com/getSubRankList?sortType=22&categoryId=-2&pageSize=20&startIndex=0&needCateList=0&phoneGuid=891204461307686912&phoneImei=862095025228963&qua=TMAF_652_F_2152%2F062152%26NA%2F062152%2F6522130_2152%265.1_22_2_0_0%26120_72_14%26Meizu_MX4_Meizu_meizumx4%261000047%262152%26V3&androidId=dba20155a97326c&macAdress=&imsi=460011431632413&wifiBssid="
    result = BsUtil.praseQQ(url)
    for app in result['appList']:
        print(app['appName'], app['apkId'], '下载数：', app['appDownCount'], '评分：', float(app['score']) * 10,
              app['packageName'])
        getData(app['appName'], app['appDownCount'], float(app['score']) * 10, app['packageName'])
    pass


if __name__ == '__main__':
    getTop()
    # getData('', 0, 0, packageName='com.qqgame.hlddz')
    DbUtil.close(conn, cur)
