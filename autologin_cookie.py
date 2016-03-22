#coding: utf-8
import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
import sys
import os
import warnings
import utils

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
import time
import cookielib
import urllib2
import urllib
import gzip, StringIO

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#参考 http://iwww.me/522.html   http://lanbing510.info/2016/03/15/Lianjia-Spider.html

# driver = webdriver.Firefox()  
driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
aim_url = "http://i.autohome.com.cn/1880254/info"
init_url = "http://account.autohome.com.cn/login"

driver.get(init_url)  

# #用户名 密码
elem_user = driver.find_element_by_name("username")  
elem_user.send_keys("longredhao")  
elem_pwd = driver.find_element_by_name("password")  
elem_pwd.send_keys("Welcome127")  
elem_pwd.send_keys(Keys.RETURN)

sendCookie = ""
for cookie in driver.get_cookies():
    sendCookie = sendCookie + cookie['name'] + "=" + cookie['value'] +";"
sendCookie = sendCookie[0:-1]
print "sendCookie:%s" %sendCookie



#会验证 Request Header 的 User-Agent 和 Referer 甚至 cookies 之类的
#修改点：User-Agent 随机选，Referer 指向来自哪里，
#发送的Headers，必须要有Cookie.下面值的获取方法：从firefox手动登录一次，然后看firebug里面的请求头信息找到的额，只是用新生成的cookie代替原来的cookie
# sendheaders = {
#         'Host':' i.autohome.com.cn',
#         'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64; rv',
#         'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Accept-Language':' zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#         'Accept-Encoding':' gzip, deflate',
#         'Cookie':' sessionfid=1608245380; __utma=1.383568587.1457674797.1457677977.1457685117.3; __utmz=1.1457674797.1.1.utmcsr=account.autohome.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/login; sessionuid=0A48A4BB-DC10-4B70-2647-1E3813C598A8||2016-03-09+17%3A31%3A41.245||0; sessionip=101.230.205.17; area=310199; sessionid=194773DA-D7DE-5C7E-96B3-766D5412B7FC%7C%7C2016-03-11+13%3A40%3A03.782%7C%7Caccount.autohome.com.cn; ref=0%7C0%7C0%7C8-1%7C2016-03-11+13%3A40%3A03.782%7C2016-03-11+13%3A40%3A03.782; pcpopclub=F6E4E27C232ACC9EABA70152BE57B4DD3BA83B8B0B78C62057FDF21A731D4F0EE8468EF19C2A63F843EFEE88DF00B0FC9F64FA4C3FF0F8DFED4C268620E76E9E5F0C53034491311E1F5303FF1951A71E8897C1A0B0B7769EC0482E9B85A03206B06E07DAEF608693194AA93B8C704B4DDEA39E060C4A1C544A26E26F3F48694A4395639C17B0ED2E531AAAD344C99FF82BEFD022419400D1C05A410D658560BC209967B6409E884E1EDF1C93DF8D6C3209629C56DDD515E27CC8F5C6B4113DF790BBAD8AAF5171B486D495ECAA7BC1AF32D7C65B0577DBFC083399A3F99445F0ED33004C1C2D77B981C0392C3F434F3757B2AF9175BAFE7A7DCB6A3BD22B9ADA6DF05E6F52D0DCF6DB63101D3F5DE8EFD04D1D7F3DF919724F3AB731F9C5DADE58D0BDDCB9F76818CED86B0B2F347C3AF3CE4907929F3D8C440882F2; clubUserShow=25918405|614|24|longredhao|0|0|0||2016-03-11 14',
#         'Connection':' keep-alive',
#         'Cache-Control':' max-age=0'
#     } 

#使用selenium得到的cookie,不行
sendheaders = {
        'Host':' i.autohome.com.cn',
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64; rv',
        'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':' zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':' gzip, deflate',
        'Connection':' keep-alive',
        'Cache-Control':' max-age=0'
    }

sendheaders['Cookie']=sendCookie  



# cookiestr = ';'.join(item for item in driver.get_cookies())  
# print cookiestr

# headers = {'cookie':cookiestr}  
req = urllib2.Request(aim_url,headers=sendheaders)
response = urllib2.urlopen(req)  
html = response.read() #gzip压缩过的数据
html = gzip.GzipFile(fileobj=StringIO.StringIO(html), mode="r")
html = html.read()

print utils.auto_detect("http://account.autohome.com.cn/")

soup = BeautifulSoup(html,"html.parser")
text = soup.select(".uData")[0].text;

print text

driver.close()
driver.quit() 





print "over"
