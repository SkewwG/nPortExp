# coding:utf-8
import nmap
from Libs.glo import *
logger = get_value('logger')        # 日志
class portScanByNmap():
    def __init__(self):
        self.Host = get_value('Host')
        self.Port = get_value('Port')
        self.nmapResult = []
        logger.info("[*] PortScan By Nmap: ")

    def scan(self):
        nmScan = nmap.PortScanner()
        nmScan.scan(self.Host, self.Port)

        # 对所有host进行扫描
        for host in nmScan.all_hosts():
            logger.info("Scanning {host}...".format(host=host))
            ret = {host: {}}

            if not nmScan[host].get("tcp", None): continue
            tcps = nmScan[host]['tcp']

            for port in tcps.keys():
                if tcps[port].get("state", None) == "open":
                    ret[host][str(port)] = tcps[port]["name"]
                    logger.info("\t[*] {host} port {port} is open \t Service is {name}".format(host=host, port=port,
                                                                                         name=tcps[port]["name"]))
            self.nmapResult.append(ret)
        set_value('nmapResult', self.nmapResult)


