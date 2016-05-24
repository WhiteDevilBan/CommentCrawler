import zlib
from bs4 import BeautifulSoup
from urllib import request
import json


def praseHtml(url):
    req = request.urlopen(url)
    return BeautifulSoup(req.read().decode('UTF-8'), "html.parser")


def praseJson(url):
    req = request.urlopen(url)

    data = req.read().decode()
    return json.loads(data)

def praseGzipJson(url):
    req = request.urlopen(url)

    result = zlib.decompress(req.read(), 16 + zlib.MAX_WBITS).decode()
    return json.loads(result)