#coding: utf-8
import requests
from bs4 import BeautifulSoup
import sys
import os
import warnings
# import MySQLdb
import mysql.connector
import datetime


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
import time
  

reload(sys);
sys.setdefaultencoding("utf-8")

driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
driver.get('http://quote.eastmoney.com/sz000009.html')

#等待需要ajax元素出现
element = WebDriverWait(driver,20).until(lambda driver: driver.find_element_by_css_selector("#hgtrun > b")) 
# element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "divuserinfo")))

#整个页面装入BS解析
soup = BeautifulSoup(driver.page_source,"html.parser")
hgtla = soup.select("#hgtla > b")[0].text;
hgtlb = soup.select("#hgtlb > b")[0].text;
hgtlc = soup.select("#hgtlc > b")[0].text;
hgtra = soup.select("#hgtra > b")[0].text;
hgtrb = soup.select("#hgtrb > b")[0].text;
hgtrc = soup.select("#hgtrc > b")[0].text;
hgtla_text = soup.select("#hgtla")[0].text;
hgtlb_text = soup.select("#hgtlb")[0].text;
hgtlc_text = soup.select("#hgtlc")[0].text;
hgtra_text = soup.select("#hgtra")[0].text;
hgtrb_text = soup.select("#hgtrb")[0].text;
hgtrc_text = soup.select("#hgtrc")[0].text;

if hgtla_text.find(u'万')>-1:
    hgtla = float(hgtla)/10000
if hgtlb_text.find(u'万')>-1:
    hgtlb = float(hgtlb)/10000
if hgtra_text.find(u'万')>-1:
    hgtra = float(hgtra)/10000
if hgtrb_text.find(u'万')>-1:
    hgtrb = float(hgtrb)/10000


total_in = float(hgtla)+float(hgtra)
total_remainder = float(hgtlb)+float(hgtrb)
total_quota = float(hgtlc)+float(hgtrc)

print "沪股通 当日资金流入: %s , 当日余额:%s ,限额:%s" % (hgtla_text,hgtlb_text,hgtlc_text)
print "港股通 当日资金流入: %s , 当日余额:%s ,限额:%s" % (hgtra_text,hgtrb_text,hgtrc_text)



date = datetime.datetime.now().strftime('%Y-%m-%d')
insert_date =  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

config = {
          'user':'chh', 
          'password':'test', 
          'host':'139.196.45.50', 
          'port':3306,  
          'database':'test'}
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

sql = "delete from tm_hugangtong where hugangtong_data_date=%s"
data = (date,)
cursor.execute(sql,data)
print "Number of rows deleted: %d" % cursor.rowcount

sql = "INSERT INTO tm_hugangtong (hugangtong_data_date,hugu_in,\
hugu_remainder,hugu_quota,ganggu_in,ganggu_remainder,ganggu_quota, \
total_in,total_remainder,total_quota,insert_date) \
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
data = (date,hgtla,hgtlb,hgtlc,hgtra,hgtrb,hgtrc,total_in,total_remainder,total_quota,insert_date)
print  data
cursor.execute(sql,data)
print "Number of rows inserted: %d" % cursor.rowcount

conn.commit()
cursor.close()
conn.close()


driver.close()
driver.quit() 
print "over"