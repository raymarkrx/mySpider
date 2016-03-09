# -*-coding:utf-8-*-

#request
#gevent
#beautifulsoup


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

#cd D:\workspace_python\mySpider
# python D:\workspace_python\mySpider\DownClass.py
#<div class="maxtitle">解答各类车险索赔事宜!!!!</div>  --帖子标题
#<div class="conttxt" xname="content">   楼主帖子  --
#<div class="x-reply font14" xname="content">  回帖 ，注意里面有引用
#<div class="pages" id="x-pages1" maxindex="67"> 每个帖子的页数，注意每个页面有2个


class DownClass():

    def __init__(self, init_url):
        #初始化实例变量
        self.q = Queue.Queue() # FIFO 
        self.threading_num = 10
        self.root_url="http://club.autohome.com.cn"
        self.root_dir = "D:/temp2"
        self.topic_id = ""
        self.enter = "\r\n"
        self.init_url = init_url
        self.err_url = self.root_dir+"/err_url.txt"
        pattern = r'forum-c-(.+?)-1.html'
        self.channel_id =re.search(pattern, init_url).group(1)
        print "dir: %s  , channel_id:%s" % (self.root_dir,self.channel_id)
        self.aim_dir = self.root_dir + "/" +self.channel_id
        
    def prepare_dir(self): 
        #删除以前的目录
        if os.path.exists(self.aim_dir):
            logging.debug( "%s is exists,remove it" % self.aim_dir)
            shutil.rmtree(self.aim_dir)
        else:
            logging.debug( "%s is not exists" % self.aim_dir )
        if os.path.exists(self.err_url):
            os.remove(self.err_url)
        os.makedirs(self.aim_dir)

    def get_url_pages(self,url):
        """得到帖子标题的所有list对应的url(根据页数循环得到),初始化queue"""
        response=requests.get(url)
        soup=BeautifulSoup(response.text,"html.parser")
        pages = soup.select(".fr")[0].text#得到页数
        url_pages=[]
        for x in xrange(1,int(pages[1:-1])+1):
            url = response.url.replace("1.html",str(x)+".html")
            url_pages.append(url)
            self.q.put(url)

        return url_pages

    def getList(self,url):
        """得到该list页的所有topic的url，调用getPages得到每个帖子的内容"""
        response=requests.get(url)
        soup=BeautifulSoup(response.text,"html.parser")
        topic_list=soup.select('div#subcontent a[href*=/bbs/thread-c-537-]')
        links = [a.attrs.get('href') for a in topic_list]
        for topic_url in links:
            self.getPages(topic_url)
            #break #只取list页面的第一个topic的url，可用于测试


    def getPages(self,topic_url):
        """得到topic所有页的内容"""
        root_url = self.root_url
        aim_dir = self.aim_dir
        topic_id = self.topic_id
        enter = self.enter
        response = requests.get(root_url + topic_url)
        charset = utils.auto_detect(root_url + topic_url)
        soup = BeautifulSoup(response.text,"html.parser")
        try:
            #得到第一页的信息
            title = soup.select(".maxtitle")[0].text;
            topic = soup.select(".conttxt .w740")[0].text;#得到楼主的topic
            tag = soup.select(".pages")[1]
            pages = tag['maxindex'] #得到页数
            #帖子ID作为文件名
            pattern = re.compile(r"thread-c-537-(.+?)-1.html")
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
                comment = self.get_comment(reply)
                logging.debug( "page 1:"+comment )
                file.write("page 1:"+utils.format_string(comment,'utf-8'))
                file.write(enter)
                file.flush()
                n=n+1
            #得到第二页以后的回帖
            if int(pages)>1:
                for page in xrange(2,int(pages)+1):
                    url=response.url.replace("1.html",str(page)+".html")
                    self.getPageOther(page,url,aim_file)
        except Exception as e:
            err_url = self.err_url
            enter = self.enter
            traceback.print_exc()
            traceback.print_exc(file=open(err_url,'w+'))
            logging.error("err_url: %s" % response.url )
            file = open(err_url,'a')
            file.write("err_url: %s" % response.url+enter)
            file.flush()
            pass
        finally:
            if 'file' in locals():
                file.close()


    def getPageOther(self,x,page_url,aim_file):
        try:
            file = open(aim_file,'a')
            enter = self.enter
            logging.debug( "页数>2的url:"+page_url +" , aim_file:"+aim_file )
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text,"html.parser")
            replys = soup.select(".w740")
            for reply in replys:
                comment = self.get_comment(reply)
                logging.debug( "page "+str(x)+":"+comment )
                file.write("page "+str(x)+":"+utils.format_string(comment,'utf-8'))
                file.write(enter)
                file.flush()
        except Exception as e:
            err_url = self.err_url
            enter = self.enter
            traceback.print_exc()
            traceback.print_exc(file=open(err_url,'w+'))
            logging.error("err_url: %s" % response.url )
            file = open(err_url,'a')
            file.write("err_url:"+response.url+enter)
            file.write(enter)
            file.flush()
            pass
        finally:
            if 'file' is locals():
                file.close()

    def get_comment(self,reply):
        i = 0
        #移除引用的评论,防止重复
        for child in reply.contents:
            if str(child).find("relyhf")>0 :
                reply.contents[i].clear()
            if str(child).find("quote") >0 :
                reply.contents[i].clear()
            i = i+1
        return reply.text

    def get_multi_thread(self):
        while not self.q.empty():
            list_url = self.q.get()
            self.getList(list_url)

    def run(self):
        """主方法"""
        start = time.time()

        self.prepare_dir()
        #初始化队列
        self.get_url_pages(self.init_url)

        #测试单页面
        #getPages("/bbs/thread-c-537-5182021-1.html")

        #单线程获取
        # for list_url in url_pages:
        #     logging.debug( list_url )
        #     getList(list_url)

        #多线程获取
        for i in range(self.threading_num):
            t = threading.Thread(target=self.get_multi_thread)
            t.start()

        end = time.time()
        logging.debug( 'Running time: %s Seconds'%(end-start) )

if __name__ == '__main__':
    start = time.time()
    #荣威550论坛 的list对应的url
    # init_url="http://club.autohome.com.cn/bbs/forum-c-537-1.html"
    # down = DownClass(init_url)
    # down.run()
    # end = time.time()
    logging.debug( 'Running time: %s Seconds'%(end-start) )