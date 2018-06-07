# -*- coding: utf-8 -*-
'''
使用的时候，主脚本 from glo import *导入该模块，然后初始化init()
其他脚本只需要 from glo import *导入模块，然后使用get_value即可。
'''

def init():
    global _global_dict
    _global_dict = {}
    _global_dict['pyVersion'] = _pyVersion() # python版本
    _global_dict['logger'] = _logger()   # 日志
    _global_dict['pwdTxtsName'] = pwdTxtsName()       # 获取密码字典名字
    _global_dict['ports_protocols'] = _ports_protocols() #端口协议
    _global_dict['serviceAdmin'] = serviceAdmin()       # 各个服务对应的管理员用户名，比如mysql的root，mssql的sa
    _global_dict['probes'] = _probes()       # 探针
    _global_dict['serviceRE'] = _service()        # 服务名和正则规则

    _global_dict['pingList'] = []  # 存放存活IP
    _global_dict['ipOpenPort'] = {}     # 存放开放端口
    _global_dict['serviceList'] = {}        # 存放探测到的服务
    _global_dict['brustPortDic'] = {}  # 存放要爆破的IP，端口，字典 eg: {'116.89.248.27': {'3306': 'dic_password_mysql.txt'}, '116.89.248.28': {'3306': 'dic_password_mysql.txt'}
    setPwdSys()                    # 添加密码文件目录到环境变量



# 设置全局变量 _global_dict的值
def set_value(key, value):
    _global_dict[key] = value

# 获取_global_dict值
def get_value(key, value=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError as e:
        return value

def exist_key(key):
    if key in _global_dict.keys():
        return True
    else:
        return False

# 添加pingList
def addPingValue(ip):
    _global_dict['pingList'].append(ip)

# 添加IP的开放端口
def addIpOpenPort(ip, port):
    if ip not in _global_dict['ipOpenPort'].keys():
        _global_dict['ipOpenPort'][ip] = [port]
    else:
        _global_dict['ipOpenPort'][ip].append(port)

# 添加探测到的服务  最终格式为：{'123.125.115.109': {'80': ['http']}, '123.125.115.111': {'80': ['http']}}
def addIpPortService(ip, port, service):
    if ip not in _global_dict['serviceList'].keys():        # ip不在字典里
        _global_dict['serviceList'][ip] = {}
        _global_dict['serviceList'][ip][port] = service
    elif port not in _global_dict['serviceList'][ip].keys():        # ip在字典里，ip的值里没有端口
        _global_dict['serviceList'][ip][port] = service
    elif service[0] not in _global_dict['serviceList'][ip][port]:       # ip在字典里，ip的值里有端口
        _global_dict['serviceList'][ip][port].extend(service)

# 版本号
def _pyVersion():
    import sys
    return 2 if sys.version[0] < '3' else 3

# 定义logger日志
def _logger():
    import logging
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关

    # 第三步，再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)  # 输出到console的log等级的开关

    # 第四步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    ch.setFormatter(formatter)

    # 第五步，将logger添加到handler里面
    logger.addHandler(ch)
    #print('!!!!!!!!logger')
    # print(logger)
    return logger

# 获取线程事件
def getThrEvent():
    import threading
    event = threading.Event()
    event.set()
    return event


# 获取字典txt名字
def pwdTxtsName():
    import os
    pwdTxtsName = os.listdir('./password/')
    return pwdTxtsName


# 端口协议
def _ports_protocols():
    ports_protocols = {
        "20": {"name": "ftp_data", "detail": "数据端口", "exp": "爆破、嗅探、溢出、后门"},
        "21": {"name": "ftp_control", "detail": "控制端口", "exp": "爆破、嗅探、溢出、后门"},
        '23': {"name": 'telnet', "detail": '远程连接', 'exp': '爆破、嗅探'},
        '25': {'name': 'smtp', 'detail': '邮件服务', 'exp': '邮件伪造'},
        '53': {'name': 'DNS', 'detail': '域名系统', 'exp': 'DNS区域传输、DNS劫持、DNS缓存投毒、DNS欺骗、深度利用：利用DNS隧道技术刺透防火墙'},
        '67': {'name': 'dhcp', 'detail': '', 'exp': '劫持、欺骗'},
        '68': {'name': 'dhcp', 'detail': '', 'exp': '劫持、欺骗'},
        '110': {'name': 'pop3', 'detail': '', 'exp': '爆破'},
        '139': {'name': 'samba', 'detail': '', 'exp': '爆破、未授权访问、远程代码执行'},
        '143': {'name': 'imap', 'detail': '', 'exp': '爆破'},
        '161': {'name': 'snmp', 'detail': '', 'exp': '爆破'},
        '389': {'name': 'ldap', 'detail': '', 'exp': '注入攻击、未授权访问'},
        '512': {'name': 'linux r', 'detail': '', 'exp': '直接使用rlogin'},
        '513': {'name': 'linux r', 'detail': '', 'exp': '直接使用rlogin'},
        '514': {'name': 'linux r', 'detail': '', 'exp': '直接使用rlogin'},
        '873': {'name': 'rsync', 'detail': '', 'exp': '未授权访问'},
        '888': {'name': 'BTLINUX', 'detail': '', 'exp': '宝塔Linux主机管理后台/默认帐户：admin|默认密码：admin'},
        '999': {'name': 'PMA', 'detail': '', 'exp': '护卫神佩带的phpmyadmin管理后台，默认帐户：root|默认密码：huweishen.com'},
        '1080': {'name': 'socket', 'detail': '', 'exp': '爆破：进行内网渗透'},
        '1352': {'name': 'lotus', 'detail': '', 'exp': '爆破：弱口令、信息泄露：源代码'},
        '1433': {'name': 'mssql', 'detail': '', 'exp': '爆破：使用系统用户登录、注入攻击'},
        '1521': {'name': 'oracle', 'detail': 'iSqlPlus Port:5560,7778', 'exp': '爆破：TNS、注入攻击'},
        '2049': {'name': 'nfs', 'detail': '', 'exp': '配置不当'},
        '2181': {'name': 'zookeeper', 'detail': '', 'exp': '未授权访问'},
        '3306': {'name': 'mysql', 'detail': '', 'exp': '爆破、拒绝服务、注入'},
        '3389': {'name': 'rdp', 'detail': '', 'exp': '爆破、Shift后门'},
        '4848': {'name': 'glassfish', 'detail': 'web中间件，admin/adminadmin', 'exp': '爆破：控制台弱口令、认证绕过'},
        '5000': {'name': 'sybase/DB2', 'detail': '', 'exp': '爆破、注入'},
        '5432': {'name': 'postgresql', 'detail': '', 'exp': '缓冲区溢出、注入攻击、爆破：弱口令'},
        '5632': {'name': 'pcanywhere', 'detail': '', 'exp': '拒绝服务、代码执行'},
        '5900': {'name': 'vnc', 'detail': '', 'exp': '爆破：弱口令、认证绕过'},
        '5901': {'name': 'vnc', 'detail': '', 'exp': '爆破：弱口令、认证绕过'},
        '5902': {'name': 'vnc', 'detail': '', 'exp': '爆破：弱口令、认证绕过'},
        '6379': {'name': 'redis', 'detail': '', 'exp': '未授权访问、爆破：弱口令'},
        '7001': {'name': 'weblogic', 'detail': '', 'exp': 'JAVA反序列化、控制台弱口令、控制台部署webshell'},
        '7002': {'name': 'weblogic', 'detail': '', 'exp': 'JAVA反序列化、控制台弱口令、控制台部署webshell'},
        '80': {'name': 'web', 'detail': '', 'exp': '常见Web攻击、控制台爆破、对应服务器版本漏洞'},
        '443': {'name': 'web', 'detail': '', 'exp': '常见Web攻击、控制台爆破、对应服务器版本漏洞'},
        '8080': {'name': 'web|Tomcat|..', 'detail': '', 'exp': '常见Web攻击、控制台爆破、对应服务器版本漏洞、Tomcat漏洞'},
        '8069': {'name': 'zabbix', 'detail': '', 'exp': '远程命令执行'},
        '9090': {'name': 'websphere', 'detail': '', 'exp': '文件泄露、爆破：控制台弱口令、Java反序列'},
        '9200': {'name': 'elasticsearch', 'detail': '', 'exp': '未授权访问、远程代码执行'},
        '9300': {'name': 'elasticsearch', 'detail': '', 'exp': '未授权访问、远程代码执行'},
        '11211': {'name': 'memcacache', 'detail': '', 'exp': '未授权访问'},
        '27017': {'name': 'mongodb', 'detail': '', 'exp': '爆破、未授权访问'},
        '27018': {'name': 'mongodb', 'detail': '', 'exp': '爆破、未授权访问'},
        '50070': {'name': 'Hadoop', 'detail': 'NameNode', 'exp': '爆破、未授权访问'},
        '50075': {'name': 'Hadoop', 'detail': 'DataNode', 'exp': '爆破、未授权访问'},
        '14000': {'name': 'Hadoop', 'detail': 'httpfs', 'exp': '爆破、未授权访问'},
        '8480': {'name': 'Hadoop', 'detail': 'journalnode', 'exp': '爆破、未授权访问'},
        '8088': {'name': 'web', 'detail': '后台', 'exp': '爆破、未授权访问'},
        '50030': {'name': 'Hadoop', 'detail': 'JobTracker', 'exp': '爆破、未授权访问'},
        '50060': {'name': 'Hadoop', 'detail': 'TaskTracker', 'exp': '爆破、未授权访问'},
        '60010': {'name': 'Hadoop', 'detail': 'master', 'exp': '爆破、未授权访问'},
        '60030': {'name': 'Hadoop', 'detail': 'regionserver', 'exp': '爆破、未授权访问'},
        '10000': {'name': 'Virtualmin/Webmin', 'detail': 'hive-server2', 'exp': '服务器虚拟主机管理系统'},
        '10003': {'name': 'Hadoop', 'detail': 'spark-jdbcserver', 'exp': '爆破、未授权访问'},
        '5984': {'name': 'couchdb', 'detail': 'http://xxx:5984/_utils/', 'exp': '未授权访问'},
        '445': {'name': 'SMB', 'detail': '', 'exp': '弱口令爆破，检测是否有ms_08067等溢出'},
        '1025': {'name': '111', 'detail': '', 'exp': 'NFS'},
        '2082': {'name': '', 'detail': '', 'exp': 'cpanel主机管理系统登陆 （国外用较多）'},
        '2083': {'name': '', 'detail': '', 'exp': 'cpanel主机管理系统登陆 （国外用较多）'},
        '2222': {'name': '', 'detail': '', 'exp': 'DA虚拟主机管理系统登陆 （国外用较多）'},
        '2601': {'name': '', 'detail': '默认密码zebra', 'exp': 'zebra路由'},
        '2604': {'name': '', 'detail': '默认密码zebra', 'exp': 'zebra路由'},
        '3128': {'name': '', 'detail': 'squid', 'exp': '代理默认端口,如果没设置口令很可能就直接漫游内网了'},
        '3311': {'name': '', 'detail': '', 'exp': 'kangle主机管理系统登陆'},
        '3312': {'name': '', 'detail': '', 'exp': 'kangle主机管理系统登陆'},
        '4440': {'name': '', 'detail': 'rundeck 弱口令:admin/admin', 'exp': '参考WooYun: 借用新浪某服务成功漫游新浪内网'},
        '6082': {'name': '', 'detail': 'varnish',
                 'exp': '参考WooYun: Varnish HTTP accelerator CLI 未授权访问易导致网站被直接篡改或者作为代理进入内网'},
        '7778': {'name': '', 'detail': 'Kloxo', 'exp': '主机控制面板登录'},
        '8083': {'name': '', 'detail': 'Vestacp', 'exp': '主机管理系统 （国外用较多）'},
        '8649': {'name': '', 'detail': 'ganglia', 'exp': ''},
        '8888': {'name': '', 'detail': 'amh/LuManager', 'exp': '主机管理系统默认端口'},
        '9000': {'name': '', 'detail': 'fcgi', 'exp': 'fcgi php执行'},
        '50000': {'name': '', 'detail': 'SAP', 'exp': '命令执行'}
    }
    return ports_protocols

# 探测
def _probes():
    PROBES = [
        '\r\n\r\n',
        'GET / HTTP/1.0\r\n\r\n',
        'GET / \r\n\r\n',
        '\x01\x00\x00\x00\x01\x00\x00\x00\x08\x08',
        '\x80\0\0\x28\x72\xFE\x1D\x13\0\0\0\0\0\0\0\x02\0\x01\x86\xA0\0\x01\x97\x7C\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0',
        '\x03\0\0\x0b\x06\xe0\0\0\0\0\0',
        '\0\0\0\xa4\xff\x53\x4d\x42\x72\0\0\0\0\x08\x01\x40\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x40\x06\0\0\x01\0\0\x81\0\x02PC NETWORK PROGRAM 1.0\0\x02MICROSOFT NETWORKS 1.03\0\x02MICROSOFT NETWORKS 3.0\0\x02LANMAN1.0\0\x02LM1.2X002\0\x02Samba\0\x02NT LANMAN 1.0\0\x02NT LM 0.12\0',
        '\x80\x9e\x01\x03\x01\x00u\x00\x00\x00 \x00\x00f\x00\x00e\x00\x00d\x00\x00c\x00\x00b\x00\x00:\x00\x009\x00\x008\x00\x005\x00\x004\x00\x003\x00\x002\x00\x00/\x00\x00\x1b\x00\x00\x1a\x00\x00\x19\x00\x00\x18\x00\x00\x17\x00\x00\x16\x00\x00\x15\x00\x00\x14\x00\x00\x13\x00\x00\x12\x00\x00\x11\x00\x00\n\x00\x00\t\x00\x00\x08\x00\x00\x06\x00\x00\x05\x00\x00\x04\x00\x00\x03\x07\x00\xc0\x06\x00@\x04\x00\x80\x03\x00\x80\x02\x00\x80\x01\x00\x80\x00\x00\x02\x00\x00\x01\xe4i<+\xf6\xd6\x9b\xbb\xd3\x81\x9f\xbf\x15\xc1@\xa5o\x14,M \xc4\xc7\xe0\xb6\xb0\xb2\x1f\xf9)\xe8\x98',
        '\x16\x03\0\0S\x01\0\0O\x03\0?G\xd7\xf7\xba,\xee\xea\xb2`~\xf3\0\xfd\x82{\xb9\xd5\x96\xc8w\x9b\xe6\xc4\xdb<=\xdbo\xef\x10n\0\0(\0\x16\0\x13\0\x0a\0f\0\x05\0\x04\0e\0d\0c\0b\0a\0`\0\x15\0\x12\0\x09\0\x14\0\x11\0\x08\0\x06\0\x03\x01\0',
        '< NTP/1.2 >\n',
        '< NTP/1.1 >\n',
        '< NTP/1.0 >\n',
        '\0Z\0\0\x01\0\0\0\x016\x01,\0\0\x08\0\x7F\xFF\x7F\x08\0\0\0\x01\0 \0:\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\04\xE6\0\0\0\x01\0\0\0\0\0\0\0\0(CONNECT_DATA=(COMMAND=version))',
        '\x12\x01\x00\x34\x00\x00\x00\x00\x00\x00\x15\x00\x06\x01\x00\x1b\x00\x01\x02\x00\x1c\x00\x0c\x03\x00\x28\x00\x04\xff\x08\x00\x01\x55\x00\x00\x00\x4d\x53\x53\x51\x4c\x53\x65\x72\x76\x65\x72\x00\x48\x0f\x00\x00',
        '\0\0\0\0\x44\x42\x32\x44\x41\x53\x20\x20\x20\x20\x20\x20\x01\x04\0\0\0\x10\x39\x7a\0\x01\0\0\0\0\0\0\0\0\0\0\x01\x0c\0\0\0\0\0\0\x0c\0\0\0\x0c\0\0\0\x04',
        '\x01\xc2\0\0\0\x04\0\0\xb6\x01\0\0\x53\x51\x4c\x44\x42\x32\x52\x41\0\x01\0\0\x04\x01\x01\0\x05\0\x1d\0\x88\0\0\0\x01\0\0\x80\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x08\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x01\0\0\x40\0\0\0\x40\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x04\0\0\0\x02\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\0\0\0\0\x01\0\0\x40\0\0\0\0\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x04\0\0\0\x03\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x80\0\0\0\x01\x08\0\0\0\x01\0\0\x40\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x10\0\0\0\x01\0\0\x80\0\0\0\x01\x10\0\0\0\x01\0\0\x80\0\0\0\x01\x04\0\0\0\x04\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x40\0\0\0\x01\x09\0\0\0\x01\0\0\x80\0\0\0\x01\x04\0\0\0\x03\0\0\x80\0\0\0\x01\0\0\0\0\0\0\0\0\0\0\0\0\x01\x04\0\0\x01\0\0\x80\0\0\0\x01\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x01\0\0\x40\0\0\0\x01\0\0\0\0\x01\0\0\x40\0\0\0\0\x20\x20\x20\x20\x20\x20\x20\x20\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x01\0\xff\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\xe4\x04\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x7f',
        '\x41\0\0\0\x3a\x30\0\0\xff\xff\xff\xff\xd4\x07\0\0\0\0\0\0test.$cmd\0\0\0\0\0\xff\xff\xff\xff\x1b\0\0\0\x01serverStatus\0\0\0\0\0\0\0\xf0\x3f\0'
    ]
    return PROBES

# 服务名和正则规则
def _service():
    SIGNS = [
        'http|^HTTP.*',         # ok
        'ssh|SSH-2.0-OpenSSH.*',        # ok
        'ssh|SSH-1.0-OpenSSH.*',
        'netbios|^\x79\x08.*BROWSE',
        'netbios|^\x79\x08.\x00\x00\x00\x00',
        'netbios|^\x05\x00\x0d\x03',
        'netbios|^\x83\x00',
        'netbios|^\x82\x00\x00\x00',
        'netbios|\x83\x00\x00\x01\x8f',
        'backdoor-fxsvc|^500 Not Loged in',
        'backdoor-shell|GET: command',
        'backdoor-shell|sh: GET:',
        'bachdoor-shell|[a-z]*sh: .* command not found',
        'backdoor-shell|^bash[$#]',
        'backdoor-shell|^sh[$#]',
        'backdoor-cmdshell|^Microsoft Windows .* Copyright .*>',
        'db2|.*SQLDB2RA',       # ok 45.114.117.56
        'db2jds|^N\x00',
        'dell-openmanage|^\x4e\x00\x0d',
        'finger|^\r\n	Line	  User',
        'finger|Line	 User',
        'finger|Login name: ',
        'finger|Login.*Name.*TTY.*Idle',
        'finger|^No one logged on',
        'finger|^\r\nWelcome',
        'finger|^finger:',
        'finger|^must provide username',
        'finger|finger: GET: ',
        'ftp|^220.*\n331',      # ok    45.114.117.43
        'ftp|^220.*\n530',
        'ftp|^220.*FTP',
        'ftp|^220 .* Microsoft .* FTP',
        'ftp|^220 Inactivity timer',
        'ftp|^220 .* UserGate',
        'http|^HTTP/0.',
        'http|^HTTP/1.',
        'http|<HEAD>.*<BODY>',
        'http|<HTML>.*',
        'http|<html>.*',
        'http|<!DOCTYPE.*',
        'http|^Invalid requested URL ',
        'http|.*<?xml',
        'http|^HTTP/.*\nServer: Apache/1',
        'http|^HTTP/.*\nServer: Apache/2',
        'http-iis|.*Microsoft-IIS',     # ok
        'http-iis|^HTTP/.*\nServer: Microsoft-IIS',
        'http-iis|^HTTP/.*Cookie.*ASPSESSIONID',
        'http-iis|^<h1>Bad Request .Invalid URL.</h1>',
        'http-jserv|^HTTP/.*Cookie.*JServSessionId',
        'http-tomcat|^HTTP/.*Cookie.*JSESSIONID',
        'http-weblogic|^HTTP/.*Cookie.*WebLogicSession',
        'http-vnc|^HTTP/.*VNC desktop',
        'http-vnc|^HTTP/.*RealVNC/',
        'ldap|^\x30\x0c\x02\x01\x01\x61',   # 沒探測出來，45.114.118.238,45.114.118.247
        'ldap|^\x30\x32\x02\x01',
        'ldap|^\x30\x33\x02\x01',
        'ldap|^\x30\x38\x02\x01',
        'ldap|^\x30\x84',
        'ldap|^\x30\x45',
        'smb|^\0\0\0.\xffSMBr\0\0\0\0.*',
        'rdp|^\x03\x00\x00\x13',            # 沒探測出來
        'msrdp|^\x03\x00\x00\x0b',
        'msrdp|^\x03\x00\x00\x11',
        'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\x12.\0$',
        'msrdp|^\x03\0\0\x17\x08\x02\0\0Z~\0\x0b\x05\x05@\x06\0\x08\x91J\0\x02X$',
        'msrdp|^\x03\0\0\x11\x08\x02..}\x08\x03\0\0\xdf\x14\x01\x01$',
        'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\x03.\0$',
        'msrdp|^\x03\0\0\x0b\x06\xd0\0\0\0\0\0',
        'msrdp|^\x03\0\0\x0e\t\xd0\0\0\0[\x02\xa1]\0\xc0\x01\n$',
        'msrdp|^\x03\0\0\x0b\x06\xd0\0\x004\x12\0',
        'msrdp-proxy|^nmproxy: Procotol byte is not 8\n$',
        'msrpc|^\x05\x00\x0d\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00',
        'msrpc|\x05\0\r\x03\x10\0\0\0\x18\0\0\0....\x04\0\x01\x05\0\0\0\0$',
        'mssql|^\x04\x01\0C..\0\0\xaa\0\0\0/\x0f\xa2\x01\x0e.*',
        'mssql|^\x05\x6e\x00',                                                      # 沒探測出來
        'mssql|^\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15.*',
        'mssql|^\x04\x01\x00.\x00\x00\x01\x00\x00\x00\x15.*',
        'mssql|^\x04\x01\x00\x25\x00\x00\x01\x00\x00\x00\x15.*',
        'mssql|^\x04\x01\x00.\x00\x00\x01\x00\x00\x00\x15.*',
        'mssql|^\x04\x01\0\x25\0\0\x01\0\0\0\x15\0\x06\x01.*',
        'mssql|^\x04\x01\x00\x25\x00\x00\x01.*',
        'telnet|^xff\xfb\x01\xff\xfb\x03\xff\xfb\0\xff\xfd.*',      # 沒探測出來
        'mssql|;MSSQLSERVER;',
        'mysql|^\x19\x00\x00\x00\x0a',
        'mysql|^\x2c\x00\x00\x00\x0a',
        'mysql|hhost \'',
        'mysql|khost \'',
        'mysql|mysqladmin',
        'mysql|whost \'',
        'mysql-blocked|^\(\x00\x00',
        'mysql-secured|this MySQL',
        'mysql|mysql',      # # ok
        'mongodb|^.*version.....([\.\d]+)',     # ok 45.114.126.4，為啥是21端口？
        'nagiosd|Sorry, you \(.*are not among the allowed hosts...',
        'nessus|< NTP 1.2 >\x0aUser:',
        'oracle-tns-listener|\(ERROR_STACK=\(ERROR=\(CODE=',
        'oracle-tns-listener|\(ADDRESS=\(PROTOCOL=',
        'oracle-dbsnmp|^\x00\x0c\x00\x00\x04\x00\x00\x00\x00',
        'oracle-https|^220- ora',
        'oracle-rmi|\x00\x00\x00\x76\x49\x6e\x76\x61',
        'oracle-rmi|^\x4e\x00\x09',
        'postgres|Invalid packet length',       # 沒探測出來
        'postgres|^EFATAL',
        'rlogin|login: ',                   # 沒探測出來
        'rlogin|rlogind: ',
        'rlogin|^\x01\x50\x65\x72\x6d\x69\x73\x73\x69\x6f\x6e\x20\x64\x65\x6e\x69\x65\x64\x2e\x0a',
        'rpc-nfs|^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00',
        'rpc|\x01\x86\xa0',
        'rpc|\x03\x9b\x65\x42\x00\x00\x00\x01',
        'rpc|^\x80\x00\x00',
        'rsync|^@RSYNCD:.*',            # 沒探測出來
        'smux|^\x41\x01\x02\x00',
        'snmp-public|\x70\x75\x62\x6c\x69\x63\xa2',
        'snmp|\x41\x01\x02',
        'socks|^\x05[\x00-\x08]\x00',
        'ssh|^SSH-',
        'ssh|^SSH-.*openssh',               # ok 45.114.117.200 2222端口
        'ssl|\x15\x03\x01\x00\x02\x02',
        'ssl|^..\x04\0.\0\x02',
        'ssl|^\x16\x03\x01..\x02...\x03\x01',       # ok 45.114.117.145
        'ssl|^\x16\x03\0..\x02...\x03\0',
        'ssl|SSL.*GET_CLIENT_HELLO',
        'ssl|-ERR .*tls_start_servertls',
        'ssl|^\x16\x03\0\0J\x02\0\0F\x03\0',
        'ssl|^\x16\x03\0..\x02\0\0F\x03\0',
        'ssl|^\x15\x03\0\0\x02\x02\.*',
        'ssl|^\x16\x03\x01..\x02...\x03\x01',
        'ssl|^\x16\x03\0..\x02...\x03\0',
        'sybase|^\x04\x01\x00',         # 沒探測出來
        'telnet|^\xff\xfd',
        'telnet|Telnet is disabled now',
        'telnet|^\xff\xfe',
        'tftp|^\x00[\x03\x05]\x00',
        'http-tomcat|.*Servlet-Engine',
        'uucp|^login: password: ',
        'vnc|^RFB.*',                   # ok 45.114.118.23
        'webmin|.*MiniServ',            # ok 45.114.117.131
        'webmin|^0\.0\.0\.0:.*:[0-9]',
        'websphere-javaw|^\x15\x00\x00\x00\x02\x02\x0a']        # 沒探測出來
    serviceList = []
    for item in SIGNS:
        (label, pattern) = item.split('|', 2)
        sign = (label, pattern)
        serviceList.append(sign)
    return serviceList

# 添加密码文件目录到环境变量
def setPwdSys():
    import sys
    sys.path.append('PwdTxt')

# 各个服务对应的管理员用户名，比如mysql的root，mssql的sa
def serviceAdmin():
    service_admin = {
        'mysql': 'root',
        'mssql': 'sa'


    }
    return service_admin