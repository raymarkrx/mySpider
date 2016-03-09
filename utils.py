# -*-coding:utf-8-*-

import chardet
import urllib2
import urllib
import random


def auto_detect(url):
    """自动检测url内容的字符集"""
    content=urllib.urlopen(url).readline()
    result=chardet.detect(content)
    encoding=result['encoding']
    return encoding

def format_string(string,charset):
    return string.decode(charset).encode('utf-8')

user_agents=[
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
]

def get_content(url):
    """获取403禁止访问的网页"""
    user_agent = random.choice(user_agents)
    req = urllib2.Request(url)
    req.add_header("Host","bbs.csdn.net")
    req.add_header("Referer","http://bbs.csdn.net/home")
    req.add_header("User-Agent",user_agent)
    req.add_header("GET",url)

    return urllib2.urlopen(req).read()

if __name__ == '__main__':
    print get_content("http://bbs.csdn.net/topics/391880483")

 

