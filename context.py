import json


class Context(object):
    """请求上下文"""
    index = -1
    handlers = []
    respone = None

    def __init__(self, env, start_response):
        self.env = env
        self.start_response = start_response

    def next(self):
        self.index += 1
        s = len(self.handlers)
        while self.index < s:
            self.handlers[self.index](self)
            self.index += 1

    def json(self, data):
        self.start_response('200 OK', [('Content-Type', 'application/json;charset=utf-8')])
        self.respone = json.dumps(data, ensure_ascii=False).encode('utf-8')

    def html(self, data):
        self.start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
        self.respone = data.encode('utf-8')
