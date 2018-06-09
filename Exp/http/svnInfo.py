# coding:utf-8
import requests
from Libs.glo import *
logger = get_value('logger')

class Exploit:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    # 加载
    def launch(self):
        try:
            url = 'http://{}:{}/.svn/entries'.format(self.ip, self.port)
            logger.info('[test] {}'.format(url))
            self.attack(url)
        except Exception as e:
            ret = '[not exist svn]'
            logger.error(ret)

    def attack(self, url):
        req = requests.get(url, timeout=10)
        if req.status_code != 200:
            ret = '[not exist svn]'
        elif req.headers.get("Content-Type") == "application/octet-stream":
            ret = '[+] {} --> svn'.format(url)
        else:
            ret = '[not exist svn]'
        logger.info(ret)

# print(Exploit(r'www.ttrar.com', 80).launch())
