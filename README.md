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

pip install MySQL-python ---需要C++的库，安装麻烦，用mysql-connector-python代替
pip install selenium
安装 Phantomjs ：Phantomjs是自包含的，不需要安装其他的组件，把bin/phantomjs 放到PATH下就可以了（linux和windows版本的都一样）


 ps -ef|grep phantomjs|grep -v grep|awk '{print $2}'|xargs kill -9

测试：
python /cygdrive/d/workspace_python/mySpider/test.py
python d:\workspace_python\mySpider\test.py

周五：
沪股通 当日资金流入: 13.32亿 , 当日余额:116.68亿 ,限额:130亿
港股通 当日资金流入: 4.57亿 , 当日余额:100.43亿 ,限额:105亿


常用的User-Agent:
headers = {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}

#百度爬虫，除非哪个网站不让百度爬
Baidu_spider = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
#这是我自己的agent
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36

===对付需要登录或者ajax的大招（模拟浏览器）===
最后手段——浏览器渲染。通过 phantomjs 或类似浏览器引擎
模拟浏览器的工具：
selenium  --运行本地浏览器，比较耗时,慢啊，不太适合大规模网页抓取
htmlunit--java系统的无界面浏览器，不支持python

现在使用selenium
安装：
pip install selenium


本文介绍了利用 selenium 实现动态网站数据抓取的一种方法。但需要注意的是 selenium 需要运行本地浏览器（是自动运行），比较耗时，不太适合大规模网页抓取。因此可以尝试其它的 Javascript 加载工具，如 webkit、spynner，也可以调用无界面依赖的浏览器引擎 Casperjs、 Phantomjs 等。
http://smilejay.com/2013/12/try-phantomjs-with-selenium/
抓取需要登录的网页或者ajax请求的网页，有2个方案
1. 写Web UI自动化脚本，用Selenium启动真正的浏览器（如：IE、Firefox）来打开该网页，然后调用webdriver获取想要的页面元素。
2. 找一种浏览器渲染引擎，能够让其解析网页并执行网页中需要初始化JS，然后将JS、CSS等执行后的HTML代码输出出来。
启动真正的浏览器，可能带来两个问题：一个是需要的时间较长，另一个是UI自动化易受干扰、不够稳定。
而第2个方法，一时没有找到特别好的库（暂用Python语言）。
根据网上的一些方案和请教同事，最后在Selenium webdriver中找到了不启动浏览器但是带基于Webkit引擎的名为“PhantomJS”的driver。后来找资料发现，LinkedIn、Twitter等知名互联网公司也在使用PhantomJS用于测试。

使用selenium+phantomjs。
driver=webdriver.PhantomJS()
然后driver.get('xxxx')打开url
driver.page_source就抓取到网页了。


====测试环境=====
python 2.7 已经安装到下面的机器上:
10.25.20.30  --作为任务分发节点
10.25.20.31  --剩下的作为任务执行节点
10.25.20.32
10.25.20.33
10.25.20.34
10.25.20.35
10.25.20.36
10.25.20.37
