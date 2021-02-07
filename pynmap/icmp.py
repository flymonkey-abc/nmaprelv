# 设ICMP定包头字段初始值
import array
import struct
import time

ICMP_DATA_STR = 56
# total size of data
ICMP_TYPE = 8
# initital values of header variables
ICMP_TYPE_IP6 = 128
# ipv6
ICMP_CODE = 0
ICMP_CHECKSUM = 0
# 校验和值
ICMP_ID = 0
ICMP_SEQ_NR = 0
# 序列号值

def _construct(id, size, ipv6):
    '''
    构造一个ICMP echo 数据包
    '''

    if ipv6:  # 构建数据包头，ipv6和ipv4对应不同头部
        header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, ICMP_CHECKSUM, ICMP_ID, ICMP_SEQ_NR + id)
    else:  # ipv4头部
        header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, ICMP_CHECKSUM,
                             ICMP_ID, ICMP_SEQ_NR + id)
    load = "__ Are you here?__"  # 填充数据字段内容

    # space for time 去掉时间字符串后的包的大小
    size -= struct.calcsize("d")
    rest = ""
    if size > len(load):
        rest = load
        size -= len(load)
    rest += size * "x"  # 将数据位剩余位填充x

    data = struct.pack('d', time.time()) + rest  # 将时间填充到数据位中
    packet = header + data  # 构建数据包
    checksum = _in_cksum(packet)  # 做校验和错误

    # costruct header with correct checksum 加入校验位后重新打包
    if ipv6:
        header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, checksum,
                             ICMP_ID, ICMP_SEQ_NR + id)
    else:
        header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, checksum,
                             ICMP_ID, ICMP_SEQ_NR + id)
    packet = header + data  # 新的packet
    return packet


def _in_cksum(packet):
    """
    校验数据段算法函数，
    """

    if len(packet) & 1:
        packet = packet + '\0'
    words = array.array('h', packet)
    sum = 0
    for word in words:
        sum += (word & 0xffff)
    hi = sum >> 16
    lo = sum & 0xffff
    sum = hi + lo
    sum = sum + (sum >> 16)
    return (~sum) & 0xffff