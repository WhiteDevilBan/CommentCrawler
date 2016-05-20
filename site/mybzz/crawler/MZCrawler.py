import html
from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


def getData(id,package_name):

    total = BsUtil.praseJson('http://app.flyme.cn/apps/public/evaluate/list?app_id=%s&start=0&max=1' % id)
    conn,cur = DbUtil.getConn()

    totalComCount = total['value']['totalCount']
    # 获取总下载量和评分
    soup = BsUtil.praseHtml('http://app.flyme.cn/games/public/detail?package_name=%s' % package_name)

    totalScore = soup.find('div', class_="star_bg").attrs['data-num']
    totalDownload = soup.find(text="下      载：").parent.next_sibling.next_sibling.string
    #获取游戏名
    for child in soup.find('div', class_="detail_top").children:
        if (child.name == 'h3'):
            game_name = child.string

    cur.execute('INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
          'VALUES ("%s", "%s", "%s", "%s", "%s", "%s");' %(game_name,'meizu',totalComCount,
            totalScore,totalDownload,DateUtil.currentDate()))
    game_id = cur.lastrowid
    #获取所有评论内容
    value = BsUtil.praseJson('http://app.flyme.cn/apps/public/evaluate/list?app_id=%s&start=0&max=%s'% (id,totalComCount))

    for com in value['value']['list']:
        comment = html.unescape(com['comment']).replace("\"","'")
        time = com['create_time']
        author = html.unescape(com['user_name']).replace("\"","'")
        score = com['star']

        try:
            cur.execute('INSERT INTO comment(game_id, content, comment_time, author, score) '
                    'VALUES ("%s", "%s", "%s", "%s", %d);' % (game_id,comment,time,author,score))
        except:
            pass

    conn.commit()
    DbUtil.close(conn,cur)


def getTop50():
    result = BsUtil.praseJson('http://api-game.meizu.com/games/public/top/layout?start=0&max=50')
    for game in result['value']['blocks'][0]['data'][3:4]:
        print('游戏名：%s,id：%s,包名：%s' % (game['name'],game['id'],game['package_name']))
        try:
            getData(game['id'],game['package_name'])
        except:
            pass


if __name__ == '__main__':
    getTop50()