# -*- coding: UTF-8 -*-
from Oracle.Oracle_Z import Oracle
from Xml.XML_parse import gtl
from datetime import datetime
class insert:

    def __init__(self, project_name):
        self.project_name = project_name
        user = 'C##valtest'
        password = 'Valtest123'
        dbname = "orclpdbt"
        self.O = Oracle(dbname, user, password)

    def insert_project_info(self):
        sqlsearch = "select ID from HAWKEYE.PROJECT_INFO where project_name = '" + self.project_name + "'"
        searchresult, re = self.O.__sqlsearch__(sqlsearch)
        sql = "insert into HAWKEYE.PROJECT_INFO(project_name) VALUES ('" + self.project_name + "')"
        if re == []:
            opresult, mun = self.O.__sqloperation__(sql)
            print opresult, mun
        else:
            print "已有该项目名称"
        searchresult, re = self.O.__sqlsearch__(sqlsearch)
        return re[0][0]

    def insert_case_info(self, httpalllist, product_id):
        sql = "insert into HAWKEYE.CASE_INFO(case_no,case_name,creater,adapter_version,product_id,CREATE_DATE,IS_VALID) VALUES(:case_no, :case_name, :creater, :adapter_version, :product_id,:CREATE_DATE,:IS_VALID)"
        param = httpalllist
        for i in param:
            ts = datetime.now()
            i["adapter_version"] = "all"
            i["product_id"] = product_id
            i["IS_VALID"] = 0
            i["CREATE_DATE"] = ts
        # print param
        opresult, mun = self.O.__sqloperation__(sql,param)
        return opresult, mun

    def insert_failed_case_info(self, httpfaillist, product_id):
        sql = "insert into HAWKEYE.FAILED_CASE_INFO(case_no, RESULT_SET_ID, test_type, run_date, CREATE_DATE, run_evn, product_id, fail_cause, CAUSE_TYPE_ID) VALUES(:case_no, :RESULT_SET_ID, :test_type, :run_date, :CREATE_DATE, :run_evn, :product_id, :fail_cause, :CAUSE_TYPE_ID)"
        param = httpfaillist
        sql_result = "select max(id) from HAWKEYE.RESULT_SET"
        searchresult, re = self.O.__sqlsearch__(sql_result)
        for i in param:
            ts = datetime.now()
            i["test_type"] = 1
            i["product_id"] = product_id
            i["run_evn"] = 3
            i["CAUSE_TYPE_ID"] = 1 # 失败原因id
            i["RESULT_SET_ID"] = re[0][0] # 执行id
            i["CREATE_DATE"] = ts
        opresult, mun = self.O.__sqloperation__(sql, param)
        return opresult, mun

    def insert_result_info(self, res_set):
        sql = "insert into HAWKEYE.RESULT_SET(project_id,test_type,run_case_count,fail_count,succ_count,RUN_DATE) VALUES (:project_id, :test_type, :run_case_count, :fail_count, :succ_count, :RUN_DATE)"
        for i in res_set:
            ts = datetime.now()
            i["RUN_DATE"] = ts
        opresult, mun = self.O.__sqloperation__(sql, res_set)
        return opresult, mun

    def main(self):
        test_type = 1
        g = gtl("JmeterReport.jtl", product_name)
        collection = g.getCollection(g.filename)
        httplist = g.gethttplist(collection)
        fail_count, httpalllist, httpfaillist = g.getCase_info(httplist)
        all_count = g.get_run_case_count(httplist)
        result_set = []
        res = {}

        # 插入项目，若有则不插入
        project_id = self.insert_project_info()
        print "项目ID:", project_id

        res["project_id"] = project_id
        res["test_type"] = test_type
        res["run_case_count"] = all_count
        res["fail_count"] = fail_count
        res["succ_count"] = all_count - fail_count
        result_set.append(res)

        result, mun = self.insert_result_info(result_set)
        print "插入result_set总数的结果：", result
        print "插入result_set总数的条数：", mun

        # 插入所有的用例进入case_info表
        result, mun = self.insert_case_info(httpalllist, project_id)
        print "插入所有用例的结果：", result
        print "插入的所有的用例数：", mun

        # 插入所有失败的用例进入failed_case_info表
        result, mun = self.insert_failed_case_info(httpfaillist, project_id)
        print "插入失败用例的结果：", result
        print "插入失败的用例数：", mun

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



if __name__ == '__main__':
    product_name = '小超人'
    insert = insert(product_name)
    insert.main()