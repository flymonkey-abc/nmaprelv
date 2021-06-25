#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import functools
import socket
import threading


from queue import Queue

from scaninfo import ScanInfo

print = functools.partial(print, end='')


def _tcpConnect(IP=None, PORT=None):
    '''
    tcpConnect 用于扫描开放端口，采用的方法是通过向目标IP和PORT发送TCP
    CONNECT链接，链接成功则返回1，不成功则继续进行连接,不成功返回flag=0
    '''
    ADDR = (IP, PORT)
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpCliSock.settimeout(1)
    try:

        tcpCliSock.connect(ADDR)
        flag = 1

    except Exception:

        flag = 0
    tcpCliSock.close()
    return flag


class scanThread(threading.Thread):
    '''
    从Thread派生出一个子类
    '''

    def __init__(self, queue, sel_port, inii):
        threading.Thread.__init__(self)
        self.queue = queue
        self.sel_port = sel_port
        self.num = inii

    def run(self):

        while True:

            # 从队列取值
            ip = self.queue.get(block=True, timeout=None)  # 此处会自动阻塞
            # print(ip)
            mutex.acquire()
            for port in self.sel_port:
                flag = _tcpConnect(ip, int(port))

                if flag == 1:
                    # print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    print("####IP:%s Port:%3s is connect success\n" % (ip, port))
                else:
                    # print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    print("####IP:%s Port:%3s is connect false\n" % (ip, port))
            mutex.release()

            self.queue.task_done()



def ConnectedScan(sci: ScanInfo):
    global queue
    num_threads = 2  # 开启的线程数目
    queue = Queue()  # 获得一个队列实例
    global mutex
    mutex = threading.Lock()
    worker = []
    for inii in range(num_threads):
        # worker = threading.Thread(target=scanThread,args=(queue,alive))
        t = scanThread(queue, sci.ports, inii)
        worker.append(t)
        worker[inii].setDaemon(True)  # 设定daemon属性，主线程退出，不用等待子线程
        worker[inii].start()
        print("线程%d已开启\n" % inii)
    for ip in sci.hosts:
        queue.put(ip)
    queue.join()
    print("Done")
