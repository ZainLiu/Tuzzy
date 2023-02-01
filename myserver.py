import os
import time

from werkzeug import run_simple


class Node(object):
    def __init__(self, pattern="", part="", children=None, is_wild=False):
        self.pattern = pattern
        self.part = part
        self.children = children if children else []
        self.is_wild = is_wild

    def match_child(self, part):
        """第一个匹配成功的节点，用于插入"""
        for child in self.children:
            if child.part == part or child.is_wild:
                return child
        return None

    def match_children(self, part):
        nodes = []
        for child in self.children:
            if child.part == part or child.is_wild:
                nodes.append(child)
        return nodes

    def insert(self, pattern, parts, height):
        if len(parts) == height:
            self.pattern = pattern
            return
        part = parts[height]
        child = self.match_child(part)
        if not child:
            child = Node(part=part, is_wild=(part[0] == ":") or (part == "*"))
            self.children.append(child)
        child.insert(pattern, parts, height + 1)

    def search(self, parts, height):
        if len(parts) == height or self.part.startswith("*"):
            if self.pattern == "":
                return None
            return self
        part = parts[height]
        children = self.match_children(part)
        for child in children:
            result = child.search(parts, height + 1)
            if result:
                return result
        return None


class Route(object):
    roots = dict()
    handlers = dict()

    def parse_pattern(self, pattern):
        parts = []
        vs = pattern.split("/")
        for item in vs:
            if item != "":
                parts.append(item)
                if item[0] == "*":
                    break
        return parts

    def add_route(self, method, pattern, handler):
        parts = self.parse_pattern(pattern)
        key = method + "-" + pattern
        node = self.roots.get(method, None)
        if not node:
            self.roots[method] = Node()
        self.roots[method].insert(pattern, parts, 0)
        self.handlers[key] = handler

    def get_route(self, method, path):
        search_parts = self.parse_pattern(path)
        params = dict()
        root = self.roots.get(method, None)
        if not root:
            return None, None
        node = root.search(search_parts, 0)
        if node:
            parts = self.parse_pattern(node.pattern)
            for index, part in enumerate(parts):
                if part[0] == ":":
                    params[part[1:]] = search_parts[index]
                if part[0] == "*" and len(parts) > 1:
                    params[part[1:]] = "/".join(search_parts[index:])
                    break
            return node, params
        return None, None


def sayhello(context):
    print(os.getpid())
    context.start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    print(f'hello:{context.params.get("name")}'.encode('utf-8'))
    context.respone = f'hello:{context.params.get("name")},v1'.encode('utf-8')


def sayhellov2(context):
    print(os.getpid())
    context.start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    print(f'hello:{context.params.get("name")}'.encode('utf-8'))
    context.respone = f'hello:{context.params.get("name")},v2'.encode('utf-8')


def NotFound_404(context):
    context.start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    context.respone = f"404 NOT FOUND: %{context.env.get('PATH_INFO')}\n".encode('utf-8')


def Logger():
    def inner(context):
        t = time.time()
        context.next()
        print(f"执行时间：{time.time() - t}")

    return inner


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
            run_simple("127.0.0.1", 8080, self)
        finally:
            print("启动成功".encode('utf-8'))

    def run_tcp(self):
        pass


def create_app():
    app = Engine()
    app.get("/hello/:name/haha", sayhello)
    v2 = app.group("/v1")
    v2.use(Logger())
    v2.get("/hello/:name/haha", sayhellov2)
    return app


py_gee = create_app()

if __name__ == '__main__':
    py_gee.run_http()
