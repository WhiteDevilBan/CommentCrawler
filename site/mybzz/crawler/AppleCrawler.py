import json
from urllib import request

import zlib
from bs4 import BeautifulSoup
import re
from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


def getTop(all):
    url = "https://itunes.apple.com/cn/rss/topgrossingipadapplications/limit=50/json"

    result = BsUtil.praseJson(url)
    for app in result['feed']['entry']:
        try:
            detail = all['storePlatformData']['lockup-room']['results'][app['id']['attributes']['im:id']]

            print(app['im:name']['label'], app['id']['attributes']['im:id'], detail['userRating']['ratingCount'],
                  int(detail['userRating']['value']) * 10)
        except:
            # print(app['id']['attributes']['im:id'], '............')
            pass


def getAllDetail():
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewGrouping?cc=cn&id=29099&mt=8"
    req = request.Request(url)
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36")
    req.add_header("Host", "itunes.apple.com")
    req.add_header("Connection", "keep-alive")
    req.add_header("Cache-Control", "no-cache")
    req.add_header("Accept-Encoding", "gzip, deflate, sdch")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8,en;q=0.6")
    req.add_header("Accept", "*/*")

    resp = request.urlopen(req)

    data = zlib.decompress(resp.read(), 16 + zlib.MAX_WBITS).decode()
    soup = BeautifulSoup(data, 'html.parser')

    data = soup.find(text=re.compile('its.serverData')).replace('its.serverData=', '')
    all = json.loads(data)
    # print(all['storePlatformData']['lockup-room']['results'])
    return all


def getAllDetail2():
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
    # print(data)
    soup = BeautifulSoup(data, 'html.parser')
    data = soup.find(text=re.compile('its.serverData')).replace('its.serverData=', '')
    # print(data)
    all = json.loads(data)
    # print(all['storePlatformData']['lockup-room']['results'])
    return all


if __name__ == '__main__':
    # all = getAllDetail()
    all = getAllDetail2()
    getTop(all)
