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
