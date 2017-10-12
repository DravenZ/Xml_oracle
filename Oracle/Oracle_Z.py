# -*- coding:utf8 -*-
import cx_Oracle
import sys
import os
# 添加该编码，使得能正确查询和插入汉字
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
class Oracle:
    """
        功能：连接oracle数据库并操作数据库
        作者：zhangpengfei
    """
    def __init__(self, db_name, user, password):
        """
            功能：连接oracle数据库
            参数：user,password,dbname(用户名、密码 、数据库)
            返回：__init__无返回
            作者：zhangpengfei
            """
        try:
            self.connect = cx_Oracle.connect(user, password, db_name)
        except Exception as e:
            print("Connect failed",e)

    def __sqlsearch__(self, sql):
        """
            功能：查询
            参数：sql(sql语句)
            返回：成功返回True和查询结果（list中套的元组），失败返回False和异常信息
            作者：zhangpengfei
            """
        try:
            cur = self.connect.cursor()
            x = cur.execute(sql)
            results = x.fetchall()
            cur.close()
            return True, results
        except Exception as e:
            print("search failed", e)
            return False, e

    def __sqloperation__(self, sql, params=None):
        """
            功能：查询
            参数：sql,db，params(sql语句,连接db,params参数是选填参数，若不写该参数，sql语句应该是完整无误的)
            返回：成功返回True和影响结果，失败返回False和异常信息
            作者：zhangpengfei
            """
        try:
            cr = self.connect.cursor()
            if params != None:
                cr.executemany(sql, params)
            else:
                cr.execute(sql)
            rowcount = cr.rowcount
            cr.close()
            self.connect.commit()
            return True, rowcount
        except Exception as e:
            print("sqloperation failed", e)
            return False, e
    def close(self):
        """
            功能：关闭连接
            参数：无
            返回：成功返回True和conn，失败返回False和异常信息
            作者：zhangpengfei
            """
        try:
            conn = self.connect.close()
            return True, conn
        except Exception as e:
            return False, e

if __name__ == '__main__':
    user = 'draven'
    password = 'draven123'
    dbname = "orclpdb"

    sqlselect = "select * from student"
    sqlinsert = "insert into student values(1,'zpf','男',17)"
    sqlupdate = "update student set SSEX = 'man' where SSEX = 'm'"
    sqldelete = "delete from student where SNO = 1"
    sqlinsertdml2 = 'insert into student values(:sno,:SNAME,:SSEX,:SAGE)'
    sqldeletedml2 = "delete from student where SNO = :SNO"
    sqlupdatedml2 = "update student set SAGE = :SAGE where SSEX = :SSEX"
    insertparam = [{'SNAME':'wu1', 'SNO':5,'SSEX':'m1','SAGE':18},{'SNO':6,'SNAME':'wu2','SSEX':'m2','SAGE':18}]
    deleteparam = [{'SNO':5},{'SNO':6}]
    updateparam = [{'SAGE':201,'SSEX':'m1'},{'SAGE':202,'SSEX':'m2'}]

    O = Oracle(dbname, user, password)
    # connectresult, conn = O.conn(dbname, user, password)

    # 单条插入
    opresult, mun = O.__sqloperation__(sqlinsert)
    print mun
    # 查询
    searchresult, re = O.__sqlsearch__(sqlselect)
    print("---插入后查询---")
    # print type(re)
    for i in re:
        # print type(i)
        print i

    # 单条更新
    opresult, mun = O.__sqloperation__(sqlupdate)
    print mun
    searchresult, re = O.__sqlsearch__(sqlselect)
    print("---更新后查询---")
    for i in re:
        print i

    # 单条删除
    opresult, mun = O.__sqloperation__(sqldelete)
    print mun
    searchresult, re = O.__sqlsearch__(sqlselect)
    print("---删除后查询---")
    for i in re:
        print i

    # 多条插入
    opresult, mun =O.__sqloperation__(sqlinsertdml2,  insertparam)
    print mun
    searchresult, re = O.__sqlsearch__(sqlselect)
    print("---DML2插入后查询---")
    for i in re:
        print i

    # 多条更新
    opresult, mun = O.__sqloperation__(sqlupdatedml2, updateparam)
    print mun
    searchresult, re = O.__sqlsearch__(sqlselect)
    print("---DML2更新后查询---")
    for i in re:
        print i

    # 多条删除
    opresult, mun = O.__sqloperation__(sqldeletedml2, deleteparam)
    print mun
    searchresult, re = O.__sqlsearch__(sqlselect)
    print("---DML2删除后查询---")
    for i in re:
        print i

    result, conn = O.close()
    print result, conn
