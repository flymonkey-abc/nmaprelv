class Request:
    def __init__(self, r: str):
        self.content = r
        self.method = r.split()[0]
        self.path = r.split()[1]
        self.body = r.split('\r\n\r\n')[1]

    def form_body(self):
        return self._parse_parm(self.body)

    def parse_path(self):
        index = self.path.find('?')
        if index == -1:
            return self.path, {}
        else:
            path, query_string = self.path.split('?', 1)
            query = self._parse_parm(query_string)
            return path, query

    def headers(self):
        header_content = self.content.split("\r\n\r\n", 1)[0].split('\r\n')[1:]
        result = {}
        for line in header_content:
            k, v = line.split(': ')
            # result[quote(k)] = quote(v)
            result[k] = v
        return result

    @staticmethod
    def _parse_parm(parameters):
        args = parameters.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return query


getdata = 'GET / HTTP/1.1\r\nHost: 192.168.1.109:8083\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\nAccept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
postdata = 'POST / HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.26.10\r\nAccept: */*\r\nPostman-Token: 91e5fd31-8f36-4171-ac3e-6b62372f0ab8\r\nHost: 192.168.1.109:8083\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Type: multipart/form-data; boundary=--------------------------117745339098119596203814\r\nContent-Length: 158\r\n\r\n----------------------------117745339098119596203814\r\nContent-Disposition: form-data; name="id"\r\n\r\n3\r\n----------------------------117745339098119596203814--\r\n'

# s="root ' or 1;#"
# pattern = re.compile("o\w+t")

# pattern = re.compile("'|\||&|%|\^|(--\s)|#|\\|/|;|\"")
# print(re.search(pattern,s))
# parsedata = Request(postdata)
# test = 'GET / HTTP/1.1'
# print()