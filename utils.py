import re
import socket
import nmap
import pymysql

from RequestParse import Request



def ip_validate(ip_str):
    sep = ip_str.split('.')
    if len(sep) != 4:
        return False
    for i, x in enumerate(sep):
        try:
            int_x = int(x)
            if int_x < 0 or int_x > 255:
                return False
        except ValueError as e:
            return False
    return True




def dbconnect():

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        db='rules',
        charset='utf8',
        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
    )
    cur = conn.cursor()
    return cur

def hasmatched(data: Request):
    global parm, path
    cursor = dbconnect()

    # 默认匹配url，参数
    method = data.method

    if method == "GET":
        path, parm = data.parse_path()

    if method == 'POST':
        path = data.path
        parm = data.form_body()
    # 路径
    selectsql = "select jump,reg_expr from reg_match where url = %s"
    a = cursor.execute(selectsql, (path))
    if a == 0:
        return 'accept'
    matchdata = cursor.fetchall()
    # 参数
    for item in parm.keys():
        for dbitem in matchdata:
            policy = dbitem[0]
            regx = dbitem[1]
            pattern = re.compile(regx)

            if re.search(pattern, parm[item]) is not None:
                return policy

    return 'accept'

