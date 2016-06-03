import json
from urllib import request
from bs4 import BeautifulSoup
import re
from site.mybzz.util import DbUtil
from site.mybzz.util import BsUtil
from site.mybzz.util import DateUtil


def getTop(all):
    url = "https://itunes.apple.com/cn/rss/topgrossingipadapplications/limit=50/json"

    result = BsUtil.praseJson(url)
    for app in result['feed']['entry']:
        print(app['im:name']['label'], app['id']['attributes']['im:id'])
        print(all['storePlatformData']['lockup-room']['results'][app['id']['attributes']['im:id']])



def getAllDetail():
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewGrouping?cc=cn&id=29099&mt=8"
    req = request.Request(url)
    req.add_header("User-Agent",
                   "iTunes/12.4 (Windows; Microsoft Windows 10.0 x64 Business Edition (Build 9200); x64) AppleWebKit/7601.6016.1000.1")

    resp = request.urlopen(req)

    data = resp.read().decode()
    # result = BsUtil.praseJson(url)
    soup = BeautifulSoup(data, 'html.parser')

    print(soup.prettify())
    # print(soup.script.string)
    data = soup.find(text=re.compile('its.serverData')).replace('its.serverData=', '')
    # print(data)
    all = json.loads(data)
    # print(all['storePlatformData']['lockup-room']['results'])
    return all

if __name__ == '__main__':
    all = getAllDetail()
    # getTop(all)
