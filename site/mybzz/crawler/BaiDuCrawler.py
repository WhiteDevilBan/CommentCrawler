from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


# conn, cur = DbUtil.getConn()


def getData(groupId):
    try:
        url = "http://m.baidu.com/appsrv?action=getcommentlist&native_api=1&groupid=%s&start=0&count=1" % (
            groupId)
        result = BsUtil.praseGzipJson(url)
        totalComCount = result['total_count']
        print("总评论数：", totalComCount)
        url = "http://m.baidu.com/appsrv?action=getcommentlist&native_api=1&groupid=%s&start=0&count=%s" % (
            groupId, totalComCount)
        result = BsUtil.praseGzipJson(url)

        for comment in result['data']:
            print('INSERT INTO comment(game_id, content, comment_time, author, score) '
                  'VALUES ("%s", "%s", "%s", "%s", %s);' % (
                      0, comment['content'].replace('\n', ''), DateUtil.longToStrTime(int(comment['create_time'])),
                      comment['user_name'], comment['score']))
    except:
        pass

def getTop15():
    json_result = BsUtil.praseGzipJson(
        'http://m.baidu.com/appsrv?action=ranklist&native_api=1&pu=ctv%401%2Ccfrom%401000561u%2Ccua%40gu2ki4uq-igBNE6lI5me6NNy2I_UCvhlSdNqA%2Ccuid%400u-Yu0PYH8jVavuO_a-YagiSS8lvuvu9_a2L80ufvi6kuviJlavefYamv8_6uvtz_a2etxNNB%2Ccut%40rIviC_C0vC_7uLP7NJGCjxNIB%2Cosname%40baiduappsearch&name=game')

    for app in json_result['result']['data']:
        appInfo = app['itemdata']
        print('INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
              'VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' % (
                  appInfo['sname'], 'baidu', appInfo['commentsnum'][:-2], round(int(appInfo['score']) / 20, 1),
                  appInfo['display_download'], DateUtil.currentDate()))
        getData(appInfo['groupid'])

        detailUrl = "http://m.baidu.com/appsrv?action=detail&native_api=1&docid=%s" % appInfo['docid']
        detail = BsUtil.praseGzipJson(detailUrl)

        for version in detail['result']['data']['app_moreversion']:
            getData(version['content'][0]['groupid'])
        print('------------------------------------------------------')


if __name__ == '__main__':
    getTop15()
