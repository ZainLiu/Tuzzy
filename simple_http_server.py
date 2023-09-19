import socket

from utils.http_parse import parser


class SimpleHttpServer:
    status = None
    headers = None

    def __init__(self, host, port):
        self.__sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sk.bind((host, port))
        self.__sk.listen(1)

    def start_respone(self, status, headers):
        self.status = status
        self.headers = self.headers

    def get_resp(self, resp):
        header = "HTTP/1.1 %s\r\n" % self.status
        if self.headers:
            for t in self.headers:
                header += "%s:%s\r\n" % t
        else:
            header += "%s:%s\r\n" % ('Content-Type', 'text/html;charset=utf-8')
        data = header.encode("utf-8") + b'\r\n' + resp[0]
        return data

    def run_simple(self, app):
        while True:
            client, addr = self.__sk.accept()
            data = client.recv(1024)
            request = data
            rq_line, rq_header, rq_body, _ = parser(request)
            env = dict()
            env.update(rq_line)
            env.update(rq_header)
            env["rq_data"] = rq_body
            resp_data = app(env, self.start_respone)
            resp = self.get_resp(resp_data)
            client.send(resp)

            client.close()
