import zlib
from bs4 import BeautifulSoup
from urllib import request
import json


def praseHtml(url):
    req = request.urlopen(url)
    return BeautifulSoup(req.read().decode('UTF-8'), "html.parser")


def praseJson(url, timeout= 10):
    req = request.urlopen(url, timeout=timeout)

    data = req.read().decode()
    return json.loads(data)


def praseGzipJson(url):
    req = request.urlopen(url)

    result = zlib.decompress(req.read(), 16 + zlib.MAX_WBITS).decode()
    return json.loads(result)


def praseQQ(url):
    req = request.Request(url)
    req.add_header("Referer", "http://qzs.qq.com/open/yyb/yyb_toplist/html/downtoplist.html?_ck_bid=3")
    req.add_header("Origin", "http://qzs.qq.com")
    req.add_header("Accept", "text/xml, text/html, application/xhtml+xml, image/png, text/plain, */*;q=0.8")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Linux; Android 5.1; MX4 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.117 Mobile Safari/537.36/apiLevel/22/qqdownloader/3/ft_apiLevel/1_0_0_0")
    req.add_header("Accept-Language", "zh-CN")
    req.add_header("Accept-Charset", "utf-8, iso-8859-1, utf-16, *;q=0.7")
    req.add_header("Accept-Encoding", "gzip")
    req.add_header("Connection", "keep-alive")
    req.add_header("Host", "pngweb.3g.qq.com")
    req.add_header("Q-UA2",
                   "QV=2&PL=ADR&PR=TBS&PB=GE&VE=B1&VN=1.5.1.1065&CO=X5&COVN=025489&RF=PRI&PP=com.tencent.android.qqdownloader&PPVC=6522130&RL=1152*1920&MO= MX4 &DE=PHONE&OS=5.1&API=22&CHID=0&LCID=9422")
    req.add_header("Q-GUID", "cee926d32c56b35b7aa4310013b788cb")
    req.add_header("Q-Auth", "31045b957cf33acf31e40be2f3e71c5217597676a9729f1b")

    result = request.urlopen(req)
    return json.loads(zlib.decompress(result.read(), 16 + zlib.MAX_WBITS).decode())