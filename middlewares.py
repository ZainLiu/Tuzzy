import time


def Logger():
    def inner(context):
        t = time.time()
        context.next()
        print(f"执行时间：{time.time() - t}")

    return inner