# coding:utf-8
import sys
import os
from Libs.glo import *

getcwd = get_value('getcwd')
logger = get_value('logger')
if sys.version[0] == "2":
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

class pluginInit():
    def __init__(self, service):
        self.service = service
        self.pluginpath = getcwd + r'/Exp/' + self.service
        # 添加环境变量
        sys.path.append(self.pluginpath)
        self.plugins = self.pluginAll()
        self.pwdTxts = get_value('pwdTxts')
        # print(self.pluginpath)
        # print("Add enviroment path into the System.")

    # 列出所有插件
    def pluginAll(self):
        try:
            pp = filter(lambda x: (True, False)[x[-2:] != "py" or '__init__' in x], os.listdir(self.pluginpath))
            return [p[:-3] for p in pp]
        except Exception as e:
            logger.error('not [{}] plugins. [error] : {}'.format(self.service, e))

    # 判断插件是否存在
    def pluginExist(self, pluginName):
        return pluginName in self.plugins

    # 判断服务密码是否存在
    def pwdExist(self, service):
        if service in self.pwdTxts:
            return True
        else:
            return False

    def launch(self, pluginName):
        logger.info("[*] Launch Plugin: " + pluginName)
        return __import__(pluginName)

# class urlParse():
#     @staticmethod
#     def isHttp(host):
#         h = urlparse(host)
#         if h.scheme == 'http' or h.scheme == 'https':
#             return True
#
#     @staticmethod
#     def removeHttp(host):
#         if urlParse.isHttp(host): return urlparse(host).netloc
#         else: return urlparse(host).path
#
#     @staticmethod
#     def addHttp(host):
#         if not urlParse.isHttp(host):
#             return "http://{}".format(urlParse.removeHttp(host))