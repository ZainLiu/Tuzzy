from werkzeug import run_simple

from context import Context
from router import Route
from simple_http_server import SimpleHttpServer
from views import NotFound_404


class RouterGroup(object):
    def __init__(self, prefix="", parent=None, engine=None):
        self.prefix = prefix
        self.middlewares = []
        self.parent = parent
        self.engine = engine

    def group(self, prefix):
        engine = self.engine if self.engine else self
        new_group = RouterGroup(self.prefix + prefix, self, engine)
        engine.groups.append(new_group)
        return new_group

    def add_route(self, method, comp, handler):
        pattern = self.prefix + comp
        print(f"Route {method} - {pattern}")
        if self.engine:
            self.engine.route.add_route(method, pattern, handler)
        else:
            self.route.add_route(method, pattern, handler)

    def get(self, pattern, handler):
        self.add_route("GET", pattern, handler)

    def post(self, pattern, handler):
        self.add_route("POST", pattern, handler)

    def use(self, *middlewares):
        self.middlewares.extend(middlewares)


class Engine(RouterGroup):
    route = Route()
    groups = []

    def __call__(self, env, start_response):
        # print(start_response, type(start_response))
        c = Context(env, start_response)

        path = env.get("PATH_INFO")
        method = env.get("REQUEST_METHOD")
        middlewares = []
        for group in self.groups:
            if path.startswith(group.prefix):
                middlewares.extend(group.middlewares)
        c.handlers = middlewares
        node, params = self.route.get_route(method, path)
        c.params = params
        if node:
            handler = self.route.handlers.get(f"{method}-{node.pattern}")
            c.handlers.append(handler)
        else:
            c.handlers.append(NotFound_404)
        c.next()
        return [c.respone]

    def run_http(self):
        try:
            # werkzeug提供的简易http服务器
            # run_simple("127.0.0.1", 8080, self)
            # 自己写的简易http服务器
            shs = SimpleHttpServer("127.0.0.1", 8080)
            shs.run_simple(self)
        finally:
            print("启动成功".encode('utf-8'))

    def run_tcp(self):
        pass
