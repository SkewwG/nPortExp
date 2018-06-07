import optparse
import nmap
import time

# def main():
#     parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
#     parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
#     parser.add_option('-p', dest='tgtPort', type='string', help='specify target port')
#
#     (options, args) = parser.parse_args()
#     tgtHost = options.tgtHost
#     tgtPort = options.tgtPort
#     args.append(tgtPort)
#     if (tgtHost is None) | (tgtPort is None):
#         print('You must specify a target host and port[s]!')
#         exit(0)
#     for tgport in args:
#         nmapScan(tgtHost, tgport)

def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    print('dir(nmScan): {}'.format(dir(nmScan)))
    # 'all_hosts', 'analyse_nmap_xml_scan', 'command_line', 'csv', 'get_nmap_last_output', 'has_host', 'listscan', 'nmap_version', 'scan', 'scaninfo', 'scanstats']
    print('all_hosts : {}'.format(nmScan.all_hosts()))
    print('analyse_nmap_xml_scan : {}'.format(nmScan.analyse_nmap_xml_scan()))
    # print('command_line : {}'.format(nmScan.command_line()))
    print('csv : {}'.format(nmScan.csv()))
    # print('get_nmap_last_output : {}'.format(nmScan.get_nmap_last_output()))
    # print('has_host : {}'.format(nmScan.has_host))
    # print('listscan : {}'.format(nmScan.listscan()))
    # print('nmap_version : {}'.format(nmScan.nmap_version()))
    # # print('scan : {}'.format(nmScan.scan()))
    # print('scaninfo : {}'.format(nmScan.scaninfo()))
    # print('scanstats : {}'.format(nmScan.scanstats()))


if __name__ == '__main__':
    start = time.time()
    nmapScan('www.chengyin.org', '80')
    end = time.time()
    print(end- start)

# 测试命令:
# python python-nmap.py -H  192.168.11.1 -p 80 21 23 443 445