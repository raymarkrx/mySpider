#coding: utf-8
import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
import sys
import os
import warnings

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
import time  
  
warnings.filterwarnings("ignore", category=DeprecationWarning)
reload(sys);
sys.setdefaultencoding( "utf-8" )

driver = webdriver.Firefox()
driver.get("http://account.autohome.com.cn/login")  

# #用户名 密码
elem_user = driver.find_element_by_name("username")  
elem_user.send_keys("longredhao")  
elem_pwd = driver.find_element_by_name("password")  
elem_pwd.send_keys("Welcome127")  
elem_pwd.send_keys(Keys.RETURN)  
time.sleep(5)
#cookie
# cookie = "; ".join([item["name"] + "=" + item["value"] for item in driver.get_cookies()])
# print "cookie:%s " % cookie

data = driver.title
print "title:%s" % data

aim_url = 'http://i.autohome.com.cn/1880254/info'
driver.get(aim_url)
# print "current_url:%s" % driver.current_url

elem = driver.find_element_by_class_name("uData")
print "111:"+elem.text

driver.close()
driver.quit() 
print "over"