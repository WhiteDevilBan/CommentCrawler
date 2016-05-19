import json
from urllib import request
import html

req = request.urlopen('http://app.flyme.cn/apps/public/evaluate/list?app_id=2897832&start=0&max=10&mzos=3.0&screen_size=1080x1800')

data = html.unescape(req.read().decode())
print(data)
value = json.loads(data)

# value1= json.loads(value['value'])

print(value['value']['list'][0]['comment'])