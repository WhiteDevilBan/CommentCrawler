import json
from urllib import request
import html
from bs4 import BeautifulSoup

from site.mybzz.domain.MzComment import MzComment
from site.mybzz.util import DbUtil

def getData():
    req = request.urlopen(
        'http://app.flyme.cn/apps/public/evaluate/list?app_id=3072599&start=0&max=10000')

    data = req.read().decode()
    print(data)
    value = json.loads(data)
    count = 0
    comment = MzComment()
    conn,cur = DbUtil.getConn()
    for com in value['value']['list']:
        # print('第%d个评论' % count)
        comment.comment = html.unescape(com['comment'])
        # print('内容:', comment.comment)
        comment.time = com['create_time']
        # print('时间:', comment.time)
        comment.author = html.unescape(com['user_name'])
        # print('作者:', comment.author)
        comment.score = com['star']
        # print('评分:', comment.score)
        count += 1
        print('INSERT INTO comment(game_name, content, comment_time, author, score) VALUES ("%s", "%s", "%s", "%s", %d);' % ('皇室战争',comment.comment,comment.time,comment.author,comment.score))
        cur.execute('INSERT INTO comment(game_name, content, comment_time, author, score) VALUES ("%s", "%s", "%s", "%s", %d);' % ('皇室战争',comment.comment,comment.time,comment.author,comment.score))
    conn.commit()
    comment.totalComCount = value['value']['totalCount']
    print(comment.totalComCount)
    # 获取总下载量和评分
    req2 = request.urlopen('http://app.flyme.cn/games/public/detail?package_name=com.supercell.clashroyale.mz')
    soup = BeautifulSoup(req2.read().decode('UTF-8'), "html.parser")
    comment.totalScore = soup.find('div', class_="star_bg").attrs['data-num']
    print('总评分：', comment.totalScore)
    comment.totalDownload = soup.find(text="下      载：").parent.next_sibling.next_sibling.string
    print("总下载量：", comment.totalDownload)


if __name__ == '__main__':
    getData()
