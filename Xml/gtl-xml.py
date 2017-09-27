# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
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
        # print "共有" + str(len(httpSamples)) + "个Http请求"
        return httpSamples

    def getCase_info(self,httpSamples):
        # 打印每个Http请求的详细信息
        for httpSample in httpSamples:
            if httpSample.hasAttribute("lb"):
                case_no = (httpSample.getAttribute("lb").encode("utf-8")).split('-')[0]
                case_name = (httpSample.getAttribute("lb").encode("utf-8")).split('-')[1]
                print "用例编号、用例名称: %s,%s" % (case_no,case_name)

            if httpSample.hasAttribute("tn"):
                creater = (httpSample.getAttribute("tn").encode("utf-8")).split('-')[0]
                print "用例设计人员: %s" % creater
                # sqlinsert = "insert into USER(name,pwd) VALUES ('%s','%s')" % (
                # httpSample.getAttribute("lb"), httpSample.getAttribute("tn"))
                # print sqlinsert
                # sqldb.sqlDML(sqlinsert,conn)
            # print type(httpSample)
            if httpSample.hasAttribute("rc"):
                print httpSample.getAttribute("rc")
                if httpSample.getAttribute("rc") == '200':
                    if httpSample.getElementsByTagName('assertionResult'):
                        # print (list(httpSample.getElementsByTagName('assertionResult'))[0]).getElementsByTagName('name')[0]
                        asserts = httpSample.getElementsByTagName('assertionResult')[0]
                        print asserts.getElementsByTagName('name')[0].childNodes[0].nodeValue.strip()




    # 获取用例总数
    def get_run_case_count(self,httpSamples):
        print "共有" + str(len(httpSamples)) + "个Http请求"
        return len(httpSamples)

    # def get_succ_count(self):


if __name__ == '__main__':
    g = gtl()
    collection = g.getCollection(g.filename)
    httplist = g.gethttplist(collection)
    g.getCase_info(httplist)

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