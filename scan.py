# coding:utf-8
from Libs.glo import *
init()                          # 全局变量初始化
from Libs.methods import *      # 导入方法
from Libs import nmapPortScan
import sys
logger = get_value('logger')        # 日志

# 解析输入的值，ip，线程数目，扫描端口，扫描服务
def Parse(Host, Port, threads, attack):
    set_value('threadNum', threads)      # 线程数目存入全局变量

    # ping IP
    if Host:
        set_value('Host', Host)   # Host命令存入全局变量
        logger.info('-' * 30 + 'START PARSE IP' + '-' * 30)
        # hostParse()  # 解析Host命令



    # if filesPath:
    #     set_value('filesPath', filesPath)  # files地址存入全局变量
    #     filesParse()


    # 扫描开放端口
    # if Port:
    #     set_value('Port', Port)  # 端口命令存入全局变量
    #     # portParse()            # 解析端口命令
    #     logger.info('-' * 30 + 'START SCAN PORT' + '-' * 30)
    #     nmapPortScan.portScanByNmap().scan()
    #     logger.info('开放端口：{}'.format(get_value('nmapResult')))           # {'123.125.115.109': ['80'], '123.125.115.110': ['80'], '123.125.115.111': ['80']}

    if attack:
        attackMultiThread()

if __name__ == '__main__':
    # parser = OptionParser('usage %prog -H <target host> -p <target port>')
    # parser.add_option('-H', '--Hosts',  dest='Hosts', type='string', help='specify target hosts')
    # parser.add_option('-p', '--Ports', dest='Ports', type='string', help='specify target ports')
    # parser.add_option('-t', '--Threads', dest='Threads', type='int', default=5, help='the number of threads')   # 默认线程为5
    #
    # (options, args) = parser.parse_args()
    # Hosts = options.Hosts
    # Ports = options.Ports
    # Threads = options.Threads
    # if (Hosts is None) | (Ports is None):
    #     print('You must specify a target host and port[s]!')
    #     exit(0)
    #
    # print(Hosts, Ports, Threads)

    Host = '103.78.141.122'    # 123.125.115.111/25       127.0.0.1 127.0.0.2
    # Host = r'C:\Users\Asus\Desktop\py\py3\project\PortExploit\files2.txt'
    Port = '21,22,80,443,3306,1433,3389'   # 21,22,80,443,3306,1433,3389
    threads = 1           # 线程数目
    attack = True
    Parse(Host=Host, Port=Port, threads=threads, attack=attack)        # 解析输入的命令