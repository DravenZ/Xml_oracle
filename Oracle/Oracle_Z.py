# -*- coding:utf8 -*-
import cx_Oracle   #引用模块cx_Oracle



class oracle():
    """
    连接数据库
    """
    def __init__(self, dbname, user, password):
        try:
            connect = cx_Oracle.connect(user, password, dbname)
            self.connect = connect
        except Exception as e:
            print("connect failed",e)

    # def conn(self, dbname, user, password):
    #     try:
    #         # d = cx_Oracle.makedsn(host, port, dbname)
    #         # cx_Oracle.connect()
    #         connect = cx_Oracle.connect(user, password, dbname)
    #         return True, connect
    #     except Exception as e:
    #         print("connect failed",e)
    #         return False, e

    # 查询
    def sqlsearch(self, sql, db):
        try:
            cur = db.cursor()
            x = cur.execute(sql)
            results = x.fetchall()
            cur.close()
            return True, results
        except Exception as e:
            print("search failed", e)
            return False, e

    # 增删改
    def sqloperation(self, sql, db, params = None):
        # execute dml with parameters
        try:
            cr = db.cursor()
            if params != None:
                cr.executemany(sql, params)
            else:
                cr.execute(sql)
            rowcount = cr.rowcount
            cr.close()
            db.commit()
            return True, rowcount
        except Exception as e:
            print("sqloperation failed", e)
            return False, e

if __name__ == '__main__':
    user = 'draven'
    password = 'draven123'
    host = "localhost"
    port = 1521
    dbname = "orclpdb"

    sqlselect = "select * from student"
    sqlinsert = "insert into student values(1,'zpf','m',17)"
    sqlupdate = "update student set SSEX = 'man' where SSEX = 'm'"
    sqldelete = "delete from student where SNO = 1"
    sqlinsertdml2 = 'insert into student values(:SNO,:SNAME,:SSEX,:SAGE)'
    sqldeletedml2 = "delete from student where SNO = :SNO"
    sqlupdatedml2 = "update student set SAGE = :SAGE where SSEX = :SSEX"
    insertparam = [{'SNO':5,'SNAME':'wu1','SSEX':'m1','SAGE':18},{'SNO':6,'SNAME':'wu2','SSEX':'m2','SAGE':18}]
    deleteparam = [{'SNO':5},{'SNO':6}]
    updateparam = [{'SAGE':201,'SSEX':'m1'},{'SAGE':202,'SSEX':'m2'}]

    O = oracle(dbname, user, password)
    # connectresult, conn = O.conn(dbname, user, password)

    # 单条插入
    opresult, mun = O.sqloperation(sqlinsert, O.connect)
    print mun
    # 查询
    searchresult, re = O.sqlsearch(sqlselect, O.connect)
    print("---插入后查询---")
    # print type(re)
    for i in re:
        # print type(i)
        print i

    # 单条更新
    opresult, mun = O.sqloperation(sqlupdate, O.connect)
    print mun
    searchresult, re = O.sqlsearch(sqlselect, O.connect)
    print("---更新后查询---")
    for i in re:
        print i

    # 单条删除
    opresult, mun = O.sqloperation(sqldelete, O.connect)
    print mun
    searchresult, re = O.sqlsearch(sqlselect, O.connect)
    print("---删除后查询---")
    for i in re:
        print i

    # 多条插入
    opresult, mun =O.sqloperation(sqlinsertdml2, O.connect,  insertparam)
    print mun
    searchresult, re = O.sqlsearch(sqlselect, O.connect)
    print("---DML2插入后查询---")
    for i in re:
        print i

    # 多条更新
    opresult, mun = O.sqloperation(sqlupdatedml2, O.connect, updateparam)
    print mun
    searchresult, re = O.sqlsearch(sqlselect, O.connect)
    print("---DML2更新后查询---")
    for i in re:
        print i

    # 多条删除
    opresult, mun = O.sqloperation(sqldeletedml2, O.connect, deleteparam)
    print mun
    searchresult, re = O.sqlsearch(sqlselect, O.connect)
    print("---DML2删除后查询---")
    for i in re:
        print i

    O.connect.close()
