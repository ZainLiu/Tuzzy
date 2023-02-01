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