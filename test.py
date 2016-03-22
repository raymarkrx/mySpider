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
import subprocess

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

p = subprocess.Popen(" ps -ef|grep phantomjs|grep -v grep|awk '{print $2}'|xargs kill -9")



