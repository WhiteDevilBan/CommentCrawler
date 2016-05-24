import sys

from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


def getData(name, id, commentCount, totalDownload, packageName):

    pass


def getTop50():
    result = BsUtil.praseJson(
        "http://apps.wandoujia.com/api/v1/apps?type=weeklytopgame&max=50&start=0&opt_fields=likesCount,title,packageName,installedCountStr,id,commentsCount")
    for app in result:
        print('游戏名：%s,id：%s,评论数：%s,下载量：%s,包名：%s' % (
            app['title'], app['id'], app['commentsCount'], app['installedCountStr'], app['packageName']))
        # print(app)
        if '万' in app['installedCountStr']:
            totalDownload = int(float(app['installedCountStr'][:-2]) * 10000)
        else:
            totalDownload = int(float(app['installedCountStr'][:-1]))

        getData(app['title'], app['id'], app['commentsCount'], totalDownload, app['packageName'])


if __name__ == '__main__':
    getTop50()
