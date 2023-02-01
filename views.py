import os


def sayhello(context):
    context.json({"name": context.params.get("name"), "message": "你好呀"})


def sayhellov2(context):
    context.html(f'<h1>{context.params.get("name")},v2,哈哈哈</h1>')


def NotFound_404(context):
    context.start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
    context.respone = f"404 NOT FOUND: {context.env.get('PATH_INFO')}\n".encode('utf-8')
