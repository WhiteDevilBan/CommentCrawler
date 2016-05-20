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