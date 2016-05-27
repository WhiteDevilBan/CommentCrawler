import sys

from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


def getData(name, downloadCount, score, packageName):
    contextData = ''
    url = "http://sj.qq.com/myapp/app/comment.htm?apkName=%s&contextData=%s"
    result = BsUtil.praseJson(url % (packageName, contextData))

    totalComCount = result['obj']['total']
    print(
        'INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
        'VALUES ("%s", "%s", "%s", %d, "%s", "%s");' % (
            name, 'qq', totalComCount, score, downloadCount, DateUtil.currentDate()))

    while (True):
        result = BsUtil.praseJson(url % (packageName, contextData))
        try:
            if not result['success']:
                continue
            if result['obj']['hasNext'] != 1:
                break

            for comment in result['obj']['commentDetails']:
                print('INSERT INTO comment(game_id, content, comment_time, author, score) '
                      'VALUES ("%s", "%s", "%s", "%s", %s);' % (
                          0, comment['content'].replace('\r', ''), DateUtil.longToStrTime(int(comment['createdTime'])),
                          comment['nickName'], comment['score']))
                # print(comment)
                # if comment['nickName'] == "♀少说多笑]^ω^[":
                #     print(comment)
            contextData = result['obj']['contextData']
        except:
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
    # getTop()
    getData('', 0, 0, packageName='com.qqgame.hlddz')
