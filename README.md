目的：
在分布式环境下抓取网页

要求：
python 2.7.11 （务必这个版本）
先安装python,再安装基于python的pip或者easy_install
然后在安装需要的mudule
pip install beautifulsoup4
pip install lxml
pip install chardet
pip install requests
pip install gevent  --测试（没有安装这个）


测试：
python /cygdrive/d/workspace_python/mySpider/down.py
python d:\workspace_python\mySpider\multi_process_down.py

发帖时间 ---
发帖人
发帖数
回帖数
精华帖
注册时间
来自
爱车
关注


===分布式爬虫的环境
python 2.7 已经安装到下面的机器上:
10.25.20.30  --作为任务分发节点
10.25.20.31  --剩下的作为任务执行节点
10.25.20.32
10.25.20.33
10.25.20.34
10.25.20.35
10.25.20.36
10.25.20.37
