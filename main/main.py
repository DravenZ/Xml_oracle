# -*- coding: UTF-8 -*-
from Oracle.Oracle_Z import Oracle
from Xml.XML_parse import gtl

if __name__ == '__main__':
    user = 'draven'
    password = 'draven123'
    dbname = "orclpdb"

    product_name = '小超人'
    g = gtl("JmeterReport.jtl", product_name)
    collection = g.getCollection(g.filename)
    httplist = g.gethttplist(collection)
    fail_count, httpalllist, httpfaillist = g.getCase_info(httplist)
    all_count = g.get_run_case_count(httplist)

    sqlsearch = "select * from student"
    print sqlsearch
    O = Oracle(dbname, user, password)
    searchresult, re = O.__sqlsearch__("sqlsearch")
    print re


    print "所有的用例条数：", all_count
    print "失败的用例条数：", fail_count
    print "成功的用例条数：", all_count - fail_count

    print "失败的用例信息："
    for i in httpfaillist:
        for key, value in i.items():
            print key, value

    print "所有的用例信息："
    for i in httpalllist:
        for key, value in i.items():
            print key, value