import pymysql

from site.mybzz.util import DbUtil

# conn = pymysql.connect(host="localhost", user="root", passwd="banban123", db="comment", port=3306, charset="utf8")
#
# cur = conn.cursor()
#
# cur.execute()
statement = "select * from comment"

data =DbUtil.getAllResult(statement)

for d in data:
    print("游戏名：%s,内容：%s,时间：%s" % (d[1],d[2],d[3]))