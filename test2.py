#coding: utf-8

import mysql.connector

config = {
          'user':'chh', 
          'password':'test', 
          'host':'127.0.0.1', 
          'port':3306,  
          'database':'test'}
conn = mysql.connector.connect(**config)
cur = conn.cursor()
sql = "SELECT stock_addr,stock_code,stock_name FROM tm_stock_code "
cur.execute(sql)
result_set = cur.fetchall()
if result_set:
    for row in result_set:
        print "%s, %s, %s" % (row[0],row[1],row[2])

cur.close()
conn.close()

