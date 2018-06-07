# coding:utf-8
import sys
import os

if sys.version[0] == "2":
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

class pluginInit():
    def __init__(self):
        pass

    # 列出所有插件
    def pluginAll(self):
        pass

    # 判断插件是否存在
    def pluginExist(self):
        pass

    # 加载插件
    def launch(self):
        pass

class urlParse():
    @staticmethod
    def isHttp(host):
        h = urlparse(host)
        if h.scheme == 'http' or h.scheme == 'https':
            return True

    @staticmethod
    def removeHttp(host):
        if urlParse.isHttp(host): return urlparse(host).netloc
        else: return urlparse(host).path

    @staticmethod
    def addHttp(host):
        if not urlParse.isHttp(host):
            return "http://{}".format(urlParse.removeHttp(host))