# coding:utf-8
import requests
import re
from Libs.glo import *
logger = get_value('logger')

class Exploit:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    # 加载
    def launch(self):
        try:
            url = 'http://{}:{}/.git/HEAD'.format(self.ip, self.port)
            logger.info('[test] {}'.format(url))
            self.attack(url)
        except Exception as e:
            ret = '[not exist git]'
            logger.error(ret)

    def attack(self, url):
        req = requests.get(url, timeout=10)
        if req.status_code == 200 and re.search(r'ref: refs/heads/', req.text):
            ret = '[+] {} --> git'.format(url)
        else:
            ret = '[not exist git]'
        logger.info(ret)

# print(Exploit(r'sh.grfy.net', 443).launch())