# -*-coding:utf-8-*-

# taskmanager.py

import random, time, Queue
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = Queue.Queue()
# 接收结果的队列:
result_queue = Queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
server_addr = '10.25.20.30'
manager = QueueManager(address=(server_addr, 5000), authkey='chh')
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()
# 放几个任务进去:
init_urls = []
init_urls.append("http://club.autohome.com.cn/bbs/forum-c-537-1.html")
init_urls.append("http://club.autohome.com.cn/bbs/forum-c-3857-1.html")
init_urls.append("http://club.autohome.com.cn/bbs/forum-a-100019-1.html")
init_urls.append("http://club.autohome.com.cn/bbs/forum-o-200029-1.html")

for init_url in init_urls:
    print('Put url %s...' % init_url)
    task.put(init_url)
print("任务分发完毕")
#一直运行，否则task的queue会注销
while not task.empty():
    print "%s 任务队列中未处理的url数:%s" % (time.strftime('%Y-%m-%d %H:%M:%S'),task.qsize())
    time.sleep(2)
# 关闭:
manager.shutdown()