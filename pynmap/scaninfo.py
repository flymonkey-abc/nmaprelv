from enum import Enum


class ScanTypeEnum(Enum):
    SYN_SCAN = 1
    ACK_SCAN = 2
    CONNECT_SCAN = 3


# 每个主机信息
class Host:
    pass


# 顶级抽象信息类，提供统一的信息封装
class ScanInfo:
    hosts = []
    ports = []
    scantype:ScanTypeEnum

    def __init__(self, hosts, ports, scantype):
        self.hosts = hosts
        self.ports = ports
        self.scantype = scantype
