# -*- coding:utf-8 -*-
import Queue
import threading
import sys
import time
import re

check_match_result=Queue.Queue()
# 在线程池中工作的线程
class MyThread(threading.Thread):
    def __init__(self,workQueue,timeout=0.1,**kwargs):
        threading.Thread.__init__(self,kwargs=kwargs)
        self.timeout=timeout
        self.setDaemon(True)
        self.workQueue=workQueue
        self.start()

    def run(self):
        while True:
            try:
                global event
                # 从工作队列中获取一个任务
                callable,req_arg,req_queue=self.workQueue.get(timeout=self.timeout)
                self.status,match_rule=callable(req_arg,req_queue)
                if self.status:
                    # 如果检测到，将结果保持到队列中。
                    global check_match_result
                    check_match_result.put((self.status,match_rule))
                    print self.name,self.status,req_arg
                else:
                    print type(self.status),req_arg
            except Queue.Empty:
                break
            except:
                print sys.exc_info()
                raise
    
class ThreadPool(object):
    def __init__(self,num_of_threads=10):
        self.workQueue=Queue.Queue()
        self.threads=[]
        self.__createThreadPool(num_of_threads)

    def __createThreadPool(self,num_of_threads):
        for i in range(num_of_threads):
            thread=MyThread(self.workQueue)
            self.threads.append(thread)
    
    def wait_for_complete(self):
        while len(self.threads):
            thread=self.threads.pop()
            if thread.isAlive():
                thread.join()
    
    def add_job(self,arg,req_queue):
        self.workQueue.put((self.check_match,arg,req_queue))

    def check_match(self,arg,queue):
        while True:
            try:
                one_rule=queue.get()
                if re.match(one_rule,arg,re.IGNORECASE):
                    return True,one_rule
            except Queue.Empty:
                break
            except:
                print sys.exc_info()
                raise
        return False,None
