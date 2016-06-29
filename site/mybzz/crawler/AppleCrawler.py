import json
from urllib import request

import zlib

import sys
from bs4 import BeautifulSoup
import re
from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil

conn, cur = DbUtil.getConn()


def getComment(url, game_id):
    req = request.Request(url)
    req.add_header("User-Agent",
                   "iTunes/11.0 (Windows; Microsoft Windows 7 Business Edition Service Pack 1 "
                   "(Build 7601)) AppleWebKit/536.27.1")
    result = request.urlopen(req, timeout=30)
    json_result = json.loads(result.read().decode())
    for comment in json_result['userReviewList']:
        try:
            print('INSERT INTO comment(game_id, content, comment_time, author, score) '
                  'VALUES ("%s", "%s", "%s", "%s", %s);' % (
                      game_id, comment['body'],
                      comment['date'].replace("T", " ").replace("Z", ""),
                      comment['name'], comment['rating'] * 10))
            cur.execute('INSERT INTO comment(game_id, content, comment_time, author, score) '
                        'VALUES ("%s", "%s", "%s", "%s", %s);' % (
                            game_id, comment['body'],
                            comment['date'].replace("T", " ").replace("Z", ""),
                            comment['name'], comment['rating'] * 10))
        except:
            pass


def getData(id, totalComCount, game_id):
    start = 0
    while (totalComCount > 0):
        try:
            if totalComCount > 500:
                url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?cc=cn&id=%s&displayable-kind=11&" \
                      "startIndex=%s&endIndex=%s&sort=4&appVersion=all" % (
                          id, start, (start + 500))
            else:
                url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/userReviewsRow?cc=cn&id=%s&displayable-kind=11" \
                      "&startIndex=%s&endIndex=%s&sort=4&appVersion=all" % (
                          id, start, (start + totalComCount))

            print(url)
            totalComCount = totalComCount - 500
            start = start + 500
            getComment(url, game_id)
            conn.commit()

        except:
            print("comment error")
            getComment(url, game_id)
            pass


def getTop(all):
    url = "https://itunes.apple.com/cn/rss/topgrossingipadapplications/limit=50/json"

    result = BsUtil.praseJson(url)
    for app in result['feed']['entry']:
        if app['category']['attributes']['term'] == 'Games':
            try:
                detail = all['storePlatformData']['lockup-room']['results'][app['id']['attributes']['im:id']]

                print(
                    'INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
                    'VALUES ("%s", "%s", "%s", %s, "%s", "%s");' % (
                        app['im:name']['label'], 'Apple Store', detail['userRating']['ratingCount'],
                        (detail['userRating']['value']),
                        0, DateUtil.currentDate()))
                # cur.execute(
                #     'INSERT INTO games(game_name,from_store, total_comment_count, total_score, total_download, data_date) '
                #     'VALUES ("%s", "%s", "%s", %d, "%s", "%s");' % (app['im:name']['label'], 'Apple Store',
                #                                                     detail['userRating']['ratingCount'],
                #                                                     int(detail['userRating']['value']) * 10,
                #                                                     0, DateUtil.currentDate()))
                # getData(app['id']['attributes']['im:id'], detail['userRating']['ratingCount'], cur.lastrowid)
            except:
                # print(app['id']['attributes']['im:id'], '............')
                # print(sys.exc_info()[0], ":", sys.exc_info()[1])
                pass


def getAllDetail():
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?id=29099&popId=38&genreId=36"
    req = request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36")
    req.add_header("Host", "itunes.apple.com")
    req.add_header("Connection", "keep-alive")
    req.add_header("Cache-Control", "no-cache")
    req.add_header("X-Apple-Store-Front", "143465-19,32 ab:pNOGxia1")
    req.add_header("Accept-Language", "zh-cn, zh;q=0.75, en-us;q=0.50, en;q=0.25")
    req.add_header("X-Apple-I-MD-M", "sKfpwVaN+aYhvpzdR1eEp5E1nN7xuK5Q6eEl2fcooczbWhwrTp3PTfm5AwiMZi0hucRNdGaFRU3RX+Yx")
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    req.add_header("X-Apple-I-MD-RINFO", "17106176")
    req.add_header("X-Apple-Tz", "28800")
    req.add_header("If-Modified-Since", "Fri, 03 Jun 2016 11:23:38 GMT")
    req.add_header("X-Apple-I-MD", "AAAABQAAABCRcn9HLXhoSaRR0WXm+1cmAAAAAg==")
    req.add_header("Accept-Encoding", "gzip, deflate, sdch")

    resp = request.urlopen(req)

    data = zlib.decompress(resp.read(), 16 + zlib.MAX_WBITS).decode()

    soup = BeautifulSoup(data, 'html.parser')
    data = soup.find(text=re.compile('its.serverData')).replace('its.serverData=', '')

    all = json.loads(data)

    return all


if __name__ == '__main__':
    all = getAllDetail()
    getTop(all)
    DbUtil.close(conn, cur)
