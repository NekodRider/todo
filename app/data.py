import pymysql
from flask import flash

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'yyw19980424',
    'db': 'todos',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
config_ac = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'yyw19980424',
    'db': 'accounts',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


def Register(id, name, pw):
    connection = pymysql.connect(**config_ac)
    c = connection.cursor()
    if id != "" and name != "" and pw != "":
        sql = "select * from account where id='" + id + "'"
        c.execute(sql)
        results = c.fetchall()
        if not results:
            sql = "insert into account values('" + id + "','" + name + "','" + pw + "')"
            c.execute(sql)
            connection.commit()
            connection.close()
            return True
        else:
            connection.close()
            return 1
    else:
        connection.close()
        return 2


def login_Check(id, pw):
    connection = pymysql.connect(**config_ac)
    c = connection.cursor()
    if id != "":
        sql = "select * from account where id='" + id + "'"
        c.execute(sql)
        results = c.fetchall()
        if not results:
            connection.close()
            return False
        elif results[0]['password'] == pw:
            connection.close()
            return results[0]
    else:
        connection.close()
        return False


def Post(user_id, content):
    connection = pymysql.connect(**config)
    c = connection.cursor()
    if content != " " and content and content != 'null':
        sql = "insert into todo values(NULL ,'" + user_id + "','" + content + "',0)"
        c.execute(sql)
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False


def getPost(user_id):
    connection = pymysql.connect(**config)
    c = connection.cursor()
    sql = "select id,content,status from todo WHERE user_id='" + user_id + "'"
    c.execute(sql)
    results = c.fetchall()
    connection.close()
    return results


def delete_Post(id):
    connection = pymysql.connect(**config)
    c = connection.cursor()
    if id != "":
        sql = "delete from todo where id='" + str(id) + "'"
        c.execute(sql)
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False


def done_Post(id, status):
    connection = pymysql.connect(**config)
    c = connection.cursor()
    if id != "":
        s = 1 - status
        sql = "UPDATE todo SET status='" + str(s) + "' where id='" + str(id) + "'"
        c.execute(sql)
        connection.commit()
        connection.close()
        return True
    else:
        connection.close()
        return False
