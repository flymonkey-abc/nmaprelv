# 入口函数
import getopt
import sys

import proxy
from STscan import ConnectedScan

from scaninfo import ScanInfo


def usage():
    """
    打印帮助信息
    """
    print('''
    Help information:
    Usage: python start.py [Scan Type(s)] [Port Range] target
    Scan Type:
        -sS/sT/sA: TCP SYN/Connect()/ACK scans
        -proxy: Run with The Proxy Mode
    Port Range:
        beginIndex , endIndex
    target:
        validate ipv4 address, support format like '*'
    ''')


# [('-t', 'sT'), ('-p', '10,1024')]
def parseOpts(opts):
    '''
    解析选项，返回要扫描的类型以及端口列表
    :param opts:
    :return:
    '''
    scantype = ''
    ports = [22, 443, 80]
    for option, value in opts:
        if option == '-t':
            scantype = value
        elif option == '-p':
            ports = value.split(',')

    return scantype, ports


# ['192.168.0.1', '192.168.0.108']
def parseArgs(args):
    '''
    解析参数，返回要扫描的主机列表，n组主机的集合
    :param args:
    :return: host
    '''
    hostgroup = []
    for item in args:
        if item[-1] == '*':
            temp = []
            for i in range(254):
                temp.append(item[:-1] + i)
            hostgroup.append(temp)
        else:
            hostgroup.append(item)
    return hostgroup


def paramParse():
    '''
    解析参数并封装为一个SCI类
    :return:
    '''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:p:", ["type=", "port="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    scantype, port = parseOpts(opts)
    SCI = ScanInfo(hosts=parseArgs(args), ports=port, scantype=scantype)
    return SCI


def functionSelectiion(sci: ScanInfo):
    if sci.scantype == 'sS':
        pass
    elif sci.scantype == 'sT':
        ConnectedScan(sci)
    elif sci.scantype == 'proxy':
        proxy.start()



if __name__ == '__main__':
    SCI = paramParse()
    functionSelectiion(SCI)
