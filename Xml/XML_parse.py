# -*- coding: UTF-8 -*-

# from xml.dom.minidom import parse
import xml.dom.minidom

import time

from MysqlDB.Mysql import MysqlDb
from Oracle.Oracle_Z import Oracle
#print help(Oracle)


user = 'root'
password = '123456'
host = "localhost"
port = 3306
dbname = 'test'
sqldb = MysqlDb()
conn = sqldb.conn(host, port, dbname, user, password)

# O = Oracle(dbname, user, password)
# O.__sqlsearch__(sql="",db=O.connect)


class gtl():
    # filename = "JmeterReport.jtl"

    def __init__(self, filename, product_name):
        self.filename = filename
        self.product_name = product_name

    def getCollection(self, filename):
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(filename)
        collection = DOMTree.documentElement
        return collection

    # 在集合中获取所有Http请求
    def gethttplist(self, collection):
        httpSamples = collection.getElementsByTagName("httpSample")
        httpSamples = list(httpSamples)
        # print "共有" + str(len(httpSamples)) + "个Http请求"
        return httpSamples

    def getCase_info(self, httpSamples):
        # 打印每个Http请求的详细信息
        fail_count = 0
        httpalllist = []
        httpfaillist = []
        for httpSample in httpSamples:
            httpdata = {}
            httpfaildata = {}

            if httpSample.hasAttribute("lb"):
                case_no = (httpSample.getAttribute("lb").encode("utf-8")).split('-')[0]
                case_name = (httpSample.getAttribute("lb").encode("utf-8")).split('-')[1]
                httpdata['case_no'] = case_no
                httpdata['case_name'] = case_name
                # print "用例编号、用例名称: %s,%s" % (case_no,case_name)

            if httpSample.hasAttribute("tn"):
                creater = (httpSample.getAttribute("tn").encode("utf-8")).split('-')[0]
                httpdata['creater'] = creater
                # print "用例设计人员: %s" % creater

            if httpSample.hasAttribute("rc"):
                # print httpSample.getAttribute("rc")
                if httpSample.getElementsByTagName('assertionResult'):
                    asserts = httpSample.getElementsByTagName('assertionResult')[0]
                    failure = asserts.getElementsByTagName('failure')[0].childNodes[0].nodeValue.strip()
                    error = asserts.getElementsByTagName('error')[0].childNodes[0].nodeValue.strip()
                    if error != 'false' or failure != 'false' or httpSample.getAttribute("rc") != '200':
                        fail_cause = asserts.getElementsByTagName('failureMessage')[0].childNodes[0].nodeValue.strip()
                        # 获取时间戳，截取前10位
                        timestamp = (httpSample.getAttribute("ts").encode("utf-8"))[0:10]
                        # 转换成localtime，只有是float类型才行，强制转换
                        time_local = time.localtime(float(timestamp))
                        # 转换成新的时间格式(2017-09-20 20:32:30)
                        run_date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        fail_count = fail_count + 1
                        httpfaildata['case_no'] = case_no
                        httpfaildata['case_name'] = case_name
                        httpfaildata['creater'] = creater
                        httpfaildata['fail_cause'] = fail_cause
                        httpfaildata['run_date'] = run_date
                        httpfaillist.append(httpfaildata)
            httpalllist.append(httpdata)
        return fail_count, httpalllist, httpfaillist

    # 获取用例总数
    def get_run_case_count(self, httpSamples):
        print "共有" + str(len(httpSamples)) + "个Http请求"
        return len(httpSamples)


if __name__ == '__main__':
    product_name = '小超人'
    g = gtl("JmeterReport.jtl", product_name)
    collection = g.getCollection(g.filename)
    httplist = g.gethttplist(collection)
    fail_count, httpalllist, httpfaillist = g.getCase_info(httplist)
    all_count = g.get_run_case_count(httplist)
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









