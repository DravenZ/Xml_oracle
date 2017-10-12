# -*- coding: UTF-8 -*-
from Oracle.Oracle_Z import Oracle
from Xml.XML_parse import gtl

class insert:

    def __init__(self, project_name):
        self.project_name = project_name

    def insert_project_info(self):
        sqlsearch = "select ID from PROJECT_INFO where project_name = '" + self.project_name + "'"
        searchresult, re = O.__sqlsearch__(sqlsearch)
        sql = "insert into project_info(project_name) VALUES ('" + self.project_name + "')"
        if re == []:
            opresult, mun = O.__sqloperation__(sql)
            print opresult, mun
        else:
            print "已有该项目名称"
        searchresult, re = O.__sqlsearch__(sqlsearch)
        return re[0][0]

    def insert_case_info(self, httpalllist, product_id):
        sql = "insert into \"case_info\"(\"case_no\",\"case_name\",\"creater\",\"adapter_version\",\"product_id\") VALUES(:case_no, :case_name, :creater, :adapter_version, :product_id)"
        param = httpalllist
        for i in param:
            i["adapter_version"] = "all"
            i["product_id"] = product_id
        # print param
        opresult, mun = O.__sqloperation__(sql,param)
        return opresult, mun

    def insert_failed_case_info(self, httpfaillist, product_id):
        sql = "insert into \"failed_case_info\"(\"case_no\",\"test_type\",\"run_date\",\"run_evn\",\"product_id\",\"fail_cause\") VALUES(:case_no, :test_type, :run_date, :run_evn, :product_id,:fail_cause)"
        param = httpfaillist
        for i in param:
            i["test_type"] = 1
            i["product_id"] = product_id
            i["run_evn"] = 3
        # print param
        opresult, mun = O.__sqloperation__(sql, param)
        return opresult, mun

    def insert_result_info(self, res_set):
        sql = "insert into \"result_set\"(\"project_id\",\"test_type\",\"run_case_count\",\"fail_count\",\"succ_count\") VALUES (:project_id, :test_type, :run_case_count, :fail_count, :succ_count)"
        opresult, mun = O.__sqloperation__(sql, res_set)
        return opresult, mun



if __name__ == '__main__':
    user = 'draven'
    password = 'draven123'
    dbname = "orclpdb"

    product_name = '小超人'
    test_type = 1
    g = gtl("JmeterReport.jtl", product_name)
    collection = g.getCollection(g.filename)
    httplist = g.gethttplist(collection)
    fail_count, httpalllist, httpfaillist = g.getCase_info(httplist)
    all_count = g.get_run_case_count(httplist)
    result_set = []
    res = {}

    O = Oracle(dbname, user, password)
    insert = insert(product_name)
    # 插入项目，若有则不插入
    project_id = insert.insert_project_info()
    print "项目ID:", project_id


    #插入所有的用例进入case_info表
    result, mun = insert.insert_case_info(httpalllist, project_id)
    print "插入所有用例的结果：", result
    print "插入的所有的用例数：", mun

    # 插入所有失败的用例进入failed_case_info表
    result, mun = insert.insert_failed_case_info(httpfaillist, project_id)
    print "插入失败用例的结果：", result
    print "插入失败的用例数：", mun

    res["project_id"] = project_id
    res["test_type"] = test_type
    res["run_case_count"] = all_count
    res["fail_count"] = fail_count
    res["succ_count"] = all_count - fail_count
    result_set.append(res)

    result, mun = insert.insert_result_info(result_set)
    print "插入result_set总数的结果：", result
    print "插入result_set总数的条数：", mun

    print "所有的用例条数：", all_count
    print "失败的用例条数：", fail_count
    print "成功的用例条数：", all_count - fail_count

    print "失败的用例信息："
    for i in httpfaillist:
        for key, value in i.items():
            print key, value

    print "所有的用例信息："
    print httpalllist[:3]
    for i in httpalllist:
        for key, value in i.items():
            print key, value