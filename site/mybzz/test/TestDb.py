import pymysql

from site.mybzz.util import DbUtil
from site.mybzz.util import DateUtil

conn = pymysql.connect(host="localhost", user="root", passwd="banban123", db="comment", port=3306, charset="utf8")

cur = conn.cursor()

cur.execute("INSERT INTO comment(game_name, content, comment_time, author, score)"
            " VALUES ('游戏名123', '内容123', '2016-05-19 15:56:07', 'ban', '44');")
# conn.commit()
print("VALUES (%s, %s, %s, %s, %d);" % ('游戏名123', '内容123', '2016-05-19 15:56:07', 'ban', 44))

print(DateUtil.currentTime())
# statement = "select * from comment"
#
# data =DbUtil.getAllResult(statement)

# for d in data:
#     print("游戏名：%s,内容：%s,时间：%s" % (d[1],d[2],d[3]))