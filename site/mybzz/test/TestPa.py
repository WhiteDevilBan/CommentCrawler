import json
from urllib import request
import html
from bs4 import BeautifulSoup
# req = request.urlopen('http://app.flyme.cn/apps/public/evaluate/list?app_id=2897832&start=0&max=10&mzos=3.0&screen_size=1080x1800')
#
# data = html.unescape(req.read().decode())
# print(data)
# value = json.loads(data)
#
# # value1= json.loads(value['value'])
#
# print(value['value']['list'][0]['comment'])


req2 = request.urlopen('http://app.flyme.cn/games/public/detail?package_name=com.supercell.clashroyale.mz')
soup = BeautifulSoup(req2.read().decode('UTF-8'), "html.parser")

# for div in soup.find_all('div', class_="detail_top"):
#     print(div)
# print(soup.find('div', class_="detail_top").child)
for child in soup.find('div', class_="detail_top").children:
    if(child.name=='h3'):
        print(child.string)
# game_name = soup.find('div', class_="detail_top").
# attrs['data-num']