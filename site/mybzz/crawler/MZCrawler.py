import json
from urllib import request
import html
from bs4 import BeautifulSoup


def getData():
    req = request.urlopen(
        'http://app.flyme.cn/apps/public/evaluate/list?app_id=3072599&start=0&max=1538')

    data = req.read().decode()
    print(data)
    value = json.loads(data)
    count = 0
    for comment in value['value']['list']:
        print('第%d个评论' % count)
        print('内容:', html.unescape(comment['comment']))
        print('时间:', comment['create_time'])
        print('作者:', html.unescape(comment['user_name']))
        print('评分:', comment['star'])
        count += 1
        print()

    # 获取总下载量和评分
    req2 = request.urlopen('http://app.flyme.cn/games/public/detail?package_name=com.supercell.clashroyale.mz')
    soup = BeautifulSoup(req2.read().decode('UTF-8'), "html.parser")
    page = soup.prettify()
    print('总评分：', soup.find('div', class_="star_bg").attrs['data-num'])
    print("总下载量：", soup.find(text="下      载：").parent.next_sibling.next_sibling.string)


if __name__ == '__main__':
    getData()
