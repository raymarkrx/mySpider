# -*-coding:utf-8-*-

import time, sys, Queue
from multiprocessing.managers import BaseManager
import multiProcessDown_autohome

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:
server_addr =  '10.25.20.30'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey='chh')
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:
while True:
    try:
        init_url = task.get(timeout=3)
        print('spiderworker ====init_url:%s' % (init_url))
        multiProcessDown_autohome.do(init_url)
    except Exception as e:
        print e
        break
# 处理结束:
print('worker exit.')