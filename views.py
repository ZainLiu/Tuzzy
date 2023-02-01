import os


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