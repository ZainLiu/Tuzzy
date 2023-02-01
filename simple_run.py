from middlewares import Logger
from tuzzy import Engine
from views import *


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
