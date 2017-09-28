# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

import time

from MysqlDB.Mysql import MysqlDb

user = 'root'
password = '123456'
host = "localhost"
port = 3306
dbname = 'test'
sqldb = MysqlDb()
conn = sqldb.conn(host,port,dbname,user,password)

class gtl():
    filename = "JmeterReport.jtl"
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
                        # print fail_cause
                        timestamp = httpSample.hasAttribute("ts")
                        # 转换成localtime
                        time_local = time.localtime(timestamp)
                        # 转换成新的时间格式(2016-05-05 20:28:54)
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
    def get_run_case_count(self,httpSamples):
        print "共有" + str(len(httpSamples)) + "个Http请求"
        return len(httpSamples)

    # def get_succ_count(self):


if __name__ == '__main__':
    g = gtl()
    collection = g.getCollection(g.filename)
    httplist = g.gethttplist(collection)
    failcount,httpalllist,httpfaillist = g.getCase_info(httplist)
    allcount = g.get_run_case_count(httplist)
    print "所有的用例条数：", allcount
    print "失败的用例条数：", failcount
    print "成功的用例条数：", allcount - failcount
    for i in httpfaillist:
        for key, value in i.items():
            print key, value
    for i in httpalllist:
        for key, value in i.items():
            print key, value









