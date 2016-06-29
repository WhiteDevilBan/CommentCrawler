import pymysql
import time
import datetime
from site.mybzz.util import DbUtil
from site.mybzz.util import DateUtil

# conn = pymysql.connect(host="localhost", user="root", passwd="banban123", db="comment", port=3306, charset="utf8")
#
# cur = conn.cursor()
#
# cur.execute("INSERT INTO comment(game_name, content, comment_time, author, score)"
#             " VALUES ('游戏名123', '内容123', '2016-05-19 15:56:07', 'ban', '44');")
# conn.commit()
# print("VALUES (%s, %s, %s, %s, %d);" % ('游戏名123', '内容123', '2016-05-19 15:56:07', 'ban', 44))
# print(time.localtime(1463739856))
# print(DateUtil.lomgToStrTime(1463739856))
# statement = "select * from comment"
#
# data =DbUtil.getAllResult(statement)

# for d in data:
#     print("游戏名：%s,内容：%s,时间：%s" % (d[1],d[2],d[3]))

conn, cur = DbUtil.getConn()


if __name__ == '__main__':
    comments = DbUtil.getAllResult("select * from comment where game_id = 275 limit 10000")
    file = open("c:/穿越火线_输入.txt", "w", encoding = "GBK")
    for comment in comments:
        try:
            print(comment[2])
            file.write(comment[2])
        except:
            pass
# if list:
#     print("11")
# else:
#     print("222")
