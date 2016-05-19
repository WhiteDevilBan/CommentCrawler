import pymysql
"""
数据库工具包
"""

def getConn():
    """
    获取数据库连接和游标
    :return:
    """
    conn = pymysql.connect(host="localhost", user="root", passwd="banban123", db="comment", port=3306, charset="utf8")
    cur = conn.cursor()
    return (conn,cur)

def getAllResult(statement):
    """
    获取所有结果
    :param statement:
    :return:
    """
    conn,cur = getConn()

    cur.execute(statement)
    return cur.fetchall()

#获取一条结果
def getOneResult(statement):
    """
    获取一条记录
    :param statement:
    :return:
    """
    conn, cur = getConn()

    cur.execute(statement)
    return cur.fetchone()

#关闭连接
def close(conn,cur):
    """
    关闭连接和游标
    :param conn:
    :param cur:
    :return:
    """
    cur.close
    conn.close