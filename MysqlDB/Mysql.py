# -*- coding:utf8 -*-
import MySQLdb

import sys

print sys.getdefaultencoding()
class MysqlDb():
    # 连接数据库
    def conn(self,host,port,dbname,user,password):
        try:
            #d = MySQLdb.makedsn(host, port, dbname)
            #cx_Oracle.connect()
            conn = MySQLdb.connect(host,user,password,dbname,charset = 'utf8')
            return conn
        except Exception as e:
            print("connect failed",e)

    # 查询
    def sqlsearch(self,sql,db):
        try:
            cur = db.cursor()
            x = cur.execute(sql)                   #使用cursor进行各种操作
            results = cur.fetchmany(x)
            cur.close()
            return results
        except Exception as e:
            print("search failed", e)

    # 直接增删改
    def sqlDML(self,sql, db):
        # include: insert,update,delete
        try:
            cr = db.cursor()
            cr.execute(sql)
            cr.close()
            db.commit()
        except Exception as e:
            print("sqlDML failed",e)

    # 有参数增删改
    def sqlDML2(self,sql, params, db):
        # execute dml with parameters
        try:
            cr = db.cursor()
            cr.executemany(sql, params)
            cr.close()
            db.commit()
        except Exception as e:
            print("sqlDML2 failed", e)


if __name__ == '__main__':
    user = 'root'
    password = '123456'
    host = "localhost"
    port = 3306
    dbname = 'test'


    sqlselect = "select * from USER"
    sqlinsert = "insert into USER(name,pwd) VALUES ('GetPublickey：获取公钥','吴娟--接口测试用例 1-1')"
    sqldb = MysqlDb()
    conn = sqldb.conn(host,port,dbname,user,password)
    #sqldb.sqlDML(sqlinsert,conn)
    re = sqldb.sqlsearch(sqlselect,conn)
    #print re
    for i in re:
        print type(i)
        print(i[1])