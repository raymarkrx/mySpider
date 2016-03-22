#coding: utf-8
import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
import sys
import warnings

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
import time  

warnings.filterwarnings("ignore", category=DeprecationWarning)
reload(sys);
sys.setdefaultencoding( "utf-8" )

loginpostUrl = 'http://account.autohome.com.cn/login'
headers = { 
            'Host': 'login.weibo.cn',
            'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ZHCN)',  
            'Referer' : 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt=',
           }
postData = {
            'mobile': YourName,
            origInfo.find("form").find("input",{"type":"password"})['name']: YourPsw,
            'remember':'on',
            'backURL':origInfo.find("form").find("input",{"name":"backURL"})['value'],
            'backTitle': origInfo.find("form").find("input",{"name":"backTitle"})['value'],
            'tryCount': origInfo.find("form").find("input",{"name":"tryCount"})['value'],
            'vk': origInfo.find("form").find("input",{"name":"vk"})['value'],
            'submit': origInfo.find("form").find("input",{"name":"submit"})['value'],
            }

#post 换成登录的地址，
req = requests.post(loginpostUrl, data=postData, headers=headers)
print req.headers
#换成抓取的地址
response = requests.get('http://i.autohome.com.cn/1880254/info')
print response.text
soup = BeautifulSoup(response.text,"html.parser")
userinfo = soup.find("div", id="divuserinfo")
print type(userinfo)


