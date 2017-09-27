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
    def getCollection(self,filename):
        # 使用minidom解析器打开 XML 文档
        DOMTree = xml.dom.minidom.parse(filename)
        collection = DOMTree.documentElement
        return collection

    # 在集合中获取所有Http请求
    def gethttplist(self,collection):
        httpSamples = collection.getElementsByTagName("httpSample")
        print type(httpSamples)
        httpSamples = list(httpSamples)
        print "共有" + str(len(httpSamples)) + "个Http请求"
        return httpSamples

    def getCase_info(self,httpSamples):
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
                print "用例编号、用例名称: %s,%s" % (case_no,case_name)

            if httpSample.hasAttribute("tn"):
                creater = (httpSample.getAttribute("tn").encode("utf-8")).split('-')[0]
                httpdata['creater'] = creater
                print "用例设计人员: %s" % creater

            if httpSample.hasAttribute("rc"):
                print httpSample.getAttribute("rc")
                if httpSample.getElementsByTagName('assertionResult'):
                    asserts = httpSample.getElementsByTagName('assertionResult')[0]
                    failure =  asserts.getElementsByTagName('failure')[0].childNodes[0].nodeValue.strip()
                    error = asserts.getElementsByTagName('error')[0].childNodes[0].nodeValue.strip()
                    if error != 'false' or failure != 'false' or httpSample.getAttribute("rc") != '200':
                        fail_cause = asserts.getElementsByTagName('failureMessage')[0].childNodes[0].nodeValue.strip()
                        timestamp = httpSample.hasAttribute("ts")
                        # 转换成localtime
                        time_local = time.localtime(timestamp)
                        # 转换成新的时间格式(2016-05-05 20:28:54)
                        run_date = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                        print fail_cause
                        fail_count = fail_count + 1
                        httpfaildata['case_no'] = case_no
                        httpfaildata['case_name'] = case_name
                        httpfaildata['creater'] = creater
                        httpfaildata['fail_cause'] = fail_cause
                        httpfaildata['run_date'] = run_date
                        httpfaillist.append(httpfaildata)
            httpalllist.append(httpdata)
        #print "失败的用例条数：",fail_count
        return fail_count,httpalllist,httpfaillist




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
    print "失败的用例条数：",failcount
    for i in httpfaillist:
        print i
# if collection.hasAttribute("version"):
#    print "version : %s" % collection.getAttribute("version")










   # print "*****Movie*****"
   # if movie.hasAttribute("title"):
   #    print "Title: %s" % movie.getAttribute("title")

   # type = movie.getElementsByTagName('type')[0]
   # print "Type: %s" % type.childNodes[0].data
   # format = movie.getElementsByTagName('format')[0]
   # print "Format: %s" % format.childNodes[0].data
   # rating = movie.getElementsByTagName('rating')[0]
   # print "Rating: %s" % rating.childNodes[0].data
   # description = movie.getElementsByTagName('description')[0]
   # print "Description: %s" % description.childNodes[0].data