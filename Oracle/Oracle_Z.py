# -*- coding:utf8 -*-
import cx_Oracle   #引用模块cx_Oracle



class oracle():
    # 连接数据库
    def conn(self,host,port,dbname,user,password):
        try:
            d = cx_Oracle.makedsn(host, port, dbname)
            #cx_Oracle.connect()
            connect = cx_Oracle.connect(user,password,dbname)
            return connect
        except Exception as e:
            print("connect failed",e)

    # 查询
    def sqlsearch(self,sql,db):
        try:
            cur = db.cursor()
            x = cur.execute(sql)                   #使用cursor进行各种操作
            results = x.fetchall()
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

    O = oracle()
    conn = O.conn(host,port,dbname,user,password)

    # 单条插入
    O.sqlDML(sqlinsert, conn)

    # 查询
    re = O.sqlsearch(sqlselect,conn)
    print("---插入后查询---")
    for i in re:
        print i

    # 更新
    O.sqlDML(sqlupdate,conn)

    re = O.sqlsearch(sqlselect, conn)
    print("---更新后查询---")
    for i in re:
        print i

    # 删除
    O.sqlDML(sqldelete,conn)

    re = O.sqlsearch(sqlselect, conn)
    print("---删除后查询---")
    for i in re:
        print i

    # DML2多条插入
    O.sqlDML2(sqlinsertdml2, insertparam, conn)

    re = O.sqlsearch(sqlselect, conn)
    print("---DML2插入后查询---")
    for i in re:
        print i

    # DML2 更新
    O.sqlDML2(sqlupdatedml2, updateparam, conn)

    re = O.sqlsearch(sqlselect, conn)
    print("---DML2更新后查询---")
    for i in re:
        print i

    # DML2 删除
    O.sqlDML2(sqldeletedml2, deleteparam, conn)

    re = O.sqlsearch(sqlselect, conn)
    print("---DML2删除后查询---")
    for i in re:
        print i


    conn.close()
