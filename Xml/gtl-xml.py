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

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("JmeterReport.jtl")
collection = DOMTree.documentElement
if collection.hasAttribute("version"):
   print "version : %s" % collection.getAttribute("version")

# 在集合中获取所有Http请求
httpSamples = collection.getElementsByTagName("httpSample")
httpSamples = list(httpSamples)
# print type(httpSamples)
print "共有" + str(len(httpSamples)) + "个Http请求"
# 打印每个Http请求的详细信息
for httpSample in httpSamples:
    if httpSample.hasAttribute("lb"):
        print "Http: %s" % httpSample.getAttribute("lb")
        print httpSample.getAttribute("tn")
        sqlinsert = "insert into USER(name,pwd) VALUES ('%s','%s')" % (httpSample.getAttribute("lb"),httpSample.getAttribute("tn"))
        print sqlinsert
        sqldb.sqlDML(sqlinsert,conn)






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