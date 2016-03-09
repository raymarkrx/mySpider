#coding: utf-8
import multiprocessing
import time
import requests
import sys
from bs4 import BeautifulSoup
import re
import os
import time
from multiprocessing import Pool
import traceback
import shutil
import utils
import logging
from logging.handlers import RotatingFileHandler
import Queue
import threading
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
reload(sys);
sys.setdefaultencoding( "utf-8" )

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='down.log',
                filemode='a+')

#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)





def doIt(url,aim_dir,channel_id):
    # logging.debug( "processName:%s ,url:%s" % (multiprocessing.current_process().name,url) )
    getList(url,aim_dir,channel_id)

def getList(url,aim_dir,channel_id):
    """得到该list页的所有topic的url，调用getPages得到每个帖子的内容"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    tag = 'div#subcontent a[href*=/bbs/thread-'+channel_id+'-]'
    topic_list=soup.select(tag)
    links = [a.attrs.get('href') for a in topic_list]
    for topic_url in links:
        getPages(topic_url,aim_dir)
        break #只取list页面的第一个topic的url，可用于测试

def getPages(topic_url,aim_dir):
    """得到topic所有页的内容"""

    response = requests.get(root_url + topic_url)
    charset = utils.auto_detect(root_url + topic_url)
    soup = BeautifulSoup(response.text,"html.parser")
    try:
        #得到第一页的信息
        title = soup.select(".maxtitle")[0].text;
        topic = soup.select(".conttxt .w740")[0].text;#得到楼主的topic
        tag = soup.select(".pages")[1]
        pages = tag['maxindex'] #得到页数
        #channel_id和帖子ID作为文件名
        pattern = re.compile(r"thread-(.+?)-1.html")
        topic_id =re.search(pattern, topic_url).group(1)
        aim_file = aim_dir+"/"+topic_id+".txt"
        file = open(aim_file,'w')
        file.write("url:"+response.url+enter)
        file.write("title:"+utils.format_string(title.strip(),'utf-8')+enter)
        file.write("topic:"+utils.format_string(topic.strip(),'utf-8')+enter)
        file.write("pages:"+utils.format_string(pages.strip(),'utf-8')+enter)
        #得到回帖
        replys = soup.select(".w740")
        n=1
        for reply in replys[1:]:#第一个是楼主发的topic，跳过
            comment = get_comment(reply)
            logging.debug(multiprocessing.current_process().name + " page 1:"+comment )
            file.write(" page 1:"+utils.format_string(comment,'utf-8'))
            file.write(enter)
            file.flush()
            n=n+1
        #得到第二页以后的回帖
        if int(pages)>1:
            for page in xrange(2,int(pages)+1):
                url=response.url.replace("1.html",str(page)+".html")
                getPageOther(page,url,aim_file)
    except Exception as e:
        traceback.print_exc()
        traceback.print_exc(file=open(err_url,'w+'))
        logging.error("err_url: %s" % page_url )
        file = open(err_url,'a')
        file.write("err_url: %s" % page_url+enter)
        file.flush()
        pass
    finally:
        if 'file' in locals():
            file.close()


def getPageOther(x,page_url,aim_file):
    try:
        file = open(aim_file,'a')
        logging.debug( "页数>2的url:"+page_url +" , aim_file:"+aim_file )
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text,"html.parser")
        replys = soup.select(".w740")
        for reply in replys:
            comment = get_comment(reply)
            logging.debug( multiprocessing.current_process().name+" page "+str(x)+":"+comment )
            file.write("page "+str(x)+":"+utils.format_string(comment,'utf-8'))
            file.write(enter)
            file.flush()
    except Exception as e:
        traceback.print_exc()
        traceback.print_exc(file=open(err_url,'w+'))
        logging.error("err_url: %s" % page_url )
        file = open(err_url,'a')
        file.write("err_url:"+page_url+enter)
        file.write(enter)
        file.flush()
        pass
    finally:
        if 'file' is locals():
            file.close()

def get_comment(reply):
    i = 0
    #移除引用的评论,防止重复
    for child in reply.contents:
        if str(child).find("relyhf")>0 :
            reply.contents[i].clear()
        if str(child).find("quote") >0 :
            reply.contents[i].clear()
        i = i+1
    return reply.text


def prepare_dir(aim_dir,err_url): 
    #删除以前的目录
    if os.path.exists(aim_dir):
        logging.debug( "%s is exists,remove it" % aim_dir)
        shutil.rmtree(aim_dir)
    else:
        logging.debug( "%s is not exists" % aim_dir )
    if os.path.exists(err_url):
        os.remove(err_url)
    os.makedirs(aim_dir)

def get_url_pages(url):
    """得到帖子标题的所有list对应的url(根据页数循环得到)"""
    response=requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    pages = soup.select(".fr")[0].text#得到页数
    url_pages=[]
    for x in xrange(1,int(pages[1:-1])+1):
        url = response.url.replace("1.html",str(x)+".html")
        url_pages.append(url)
    return url_pages


def do(init_url):
    print "============init_url:"+init_url
    #初始化变量
    pattern = r'forum-(.+?)-1.html'
    channel_id = re.search(pattern, init_url).group(1)
    print "channel_id:%s" % channel_id
    aim_dir = root_dir + "/" +channel_id

    prepare_dir(aim_dir,err_url)
    url_pages = get_url_pages(init_url)
    print "============aim_dir:"+aim_dir
    #测试单页面
    # getPages("/bbs/thread-c-537-5182021-1.html")

    #单线程获取
    # for list_url in url_pages:
    #     logging.debug( list_url )
    #     getList(list_url)

    #多线程获取
    cpu_cnt = multiprocessing.cpu_count()
    print "cpu_cnt:%s" % cpu_cnt
    pool = multiprocessing.Pool(cpu_cnt)
    pool.daemon = True
    for topics_url in url_pages:
        pool.apply_async(doIt, (topics_url,aim_dir,channel_id, )) 
    pool.close()
    pool.join()

#定义变量
root_url = "http://club.autohome.com.cn"
root_dir = "D:/temp2"
enter = "\r\n"
err_url = root_dir+"/err_url.txt"
init_url = ""

if __name__ == "__main__":
    #传入的变量
    init_url = "http://club.autohome.com.cn/bbs/forum-c-537-1.html"
    do(init_url)

    print "done!"