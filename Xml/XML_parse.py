# -*- coding: UTF-8 -*-

# from xml.dom.minidom import parse
import xml.dom.minidom
import time
from datetime import datetime


class gtl():

    def __init__(self, filename, product_name):
        self.filename = filename
        self.product_name = product_name

    def getCollection(self, filename):
        # 使用minidom解析器打开 XML 文档
        try:
            DOMTree = xml.dom.minidom.parse(filename)
            collection = DOMTree.documentElement
            return collection
        except Exception as e:
            print "打开文件异常",e
            return

    # 在集合中获取所有Http请求
    def gethttplist(self, collection):
        try:
            httpSamples = collection.getElementsByTagName("httpSample")
        except Exception as e:
            print "查找httpSample异常",e
            return
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
                try:
                    case_no = (httpSample.getAttribute("lb").encode("utf-8")).split('-')[0]
                    case_name = (httpSample.getAttribute("lb").encode("utf-8")).split('-')[1]
                    httpdata['case_no'] = case_no
                    httpdata['case_name'] = case_name
                    # print "用例编号、用例名称: %s,%s" % (case_no,case_name)
                except Exception as e:
                    print "用例名称和编号异常",e

            if httpSample.hasAttribute("tn"):
                try:
                    creater = (httpSample.getAttribute("tn").encode("utf-8")).split('-')[0]
                    httpdata['creater'] = creater
                    # print "用例设计人员: %s" % creater
                except Exception as e:
                    print "查找用例作者",e

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
                        run_date = datetime.strptime(run_date,"%Y-%m-%d %H:%M:%S")
                        fail_count = fail_count + 1
                        httpfaildata['case_no'] = case_no
                        # httpfaildata['case_name'] = case_name
                        # httpfaildata['creater'] = creater
                        httpfaildata['fail_cause'] = fail_cause
                        httpfaildata['run_date'] = run_date
                        httpfaillist.append(httpfaildata)
            httpalllist.append(httpdata)
        return fail_count, httpalllist, httpfaillist

    # 获取用例总数
    def get_run_case_count(self, httpSamples):
        # print "共有" + str(len(httpSamples)) + "个Http请求"
        return len(httpSamples)

if __name__ == '__main__':
    g = gtl("TestReport.jtl", "电商")
    collection = g.getCollection(g.filename)
    httplist = g.gethttplist(collection)
    fail_count, httpalllist, httpfaillist = g.getCase_info(httplist)
    all_count = g.get_run_case_count(httplist)










