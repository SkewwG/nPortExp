# coding:utf-8
# 未授权
import redis
r = redis.Redis(host='149.28.42.95', port=6379)
r.set('name', 'test')
print(r.get('name'))