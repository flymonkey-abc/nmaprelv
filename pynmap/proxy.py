import socket
import select
import sys
# C的地址 最终访问地址
import connect

to_addr = ('0.0.0.0', 8000)  # 转发的地址


class Proxy:
    def __init__(self, addr):
        self.proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.proxy.bind(addr)
        self.proxy.listen(10)
        self.inputs = [self.proxy]
        self.route = {}

    def serve_forever(self):
        print('proxy listen...')

        while 1:
            readable, _, _ = select.select(self.inputs, [], [])
            for self.sock in readable:
                if self.sock == self.proxy:
                    self.on_join()
                else:
                    data = self.sock.recv(8080)
                    if not data:
                        self.on_quit()
                    # elif self.hasattack(data):
                    else:
                        # print(data)
                        self.route[self.sock].send(data)

    def on_join(self):
        client, addr = self.proxy.accept()
        print(addr, 'connect')
        forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        forward.connect(to_addr)
        self.inputs += [client, forward]
        self.route[client] = forward
        self.route[forward] = client

    def on_quit(self):
        for s in self.sock, self.route[self.sock]:
            self.inputs.remove(s)
            del self.route[s]
            s.close()


    def hasattack(self, data):
        conn = connect.dbconnect()
        cur = conn.cursor()


if __name__ == '__main__':
    try:
        Proxy(('0.0.0.0', 8083)).serve_forever()  # 代理服务器监听的地址
    except KeyboardInterrupt:
        sys.exit(1)