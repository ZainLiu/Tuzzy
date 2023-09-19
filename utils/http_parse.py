# -*- coding:utf-8 -*-
# author:lzy
# datetime:2023/9/19 10:23
import json


def parser(request_data):
    # 获取请求的三个段：
    # 1.请求方法 URI协议 版本
    # 2.请求头(Request Header)
    # 3.请求正文
    index0 = request_data.find(b"\r\n\r\n")

    request_predata = request_data[0:index0]
    index1 = request_predata.find(b"\r\n")

    # 请求方法 URI协议 版本
    request_first_data = request_predata[0:index1].decode("utf-8")
    request_first = {}
    count = 0
    list = ["REQUEST_METHOD", 'PATH_INFO', 'version']
    for line in request_first_data.split(" "):
        if line != "":
            request_first[list[count]] = line
            count += 1
    # print("解析请求方法 URI协议 版本：",request_first)

    # 请求头(Request Header)
    request_header_data = request_predata[index1:].decode("utf-8")
    request_headers = {}
    for line in request_header_data.split("\r\n"):
        if line != "":
            line = line.replace(" ", "")
            restemp = line.split(":")
            if restemp[0] == "Host" and len(restemp) == 3:
                restemp[1] = restemp[1] + ":" + restemp[2]
            request_headers[restemp[0]] = restemp[1]
    # print("请求头(Request Header):",request_headers)

    # 请求正文
    request_nextdata = request_data[index0:].decode("utf-8")
    request_content_temp = request_nextdata.replace("\r\n", "")
    request_content = None
    if request_content_temp != "":

        try:
            request_content = json.loads(request_content_temp)
        except:
            request_content = {'content': request_content_temp}

        # print("请求正文:",request_content)
    else:
        pass
        # print("无请求正文！")
    return request_first, request_headers, request_content, request_nextdata


def update_first_data(request_first_data, field, data):
    request_first_data[field] = data


def update_request_headers(request_headers, field, data):
    request_headers[field] = data


def update_request_content(request_content, field, data):
    request_content[field] = data


def encode(request_first_data, request_headers, request_content):
    request_data = b""
    list = ["REQUEST_METHOD", 'PATH_INFO', 'version']
    for key in list:
        request_data += (request_first_data[key] + " ").encode("utf-8")
    request_data += "\r\n".encode("utf-8")
    for key in request_headers.keys():
        request_data += (key + ":" + request_headers[key]).encode("utf-8")
        request_data += "\r\n".encode("utf-8")
    request_data += "\r\n".encode("utf-8")
    if request_content != None:
        request_data += json.dumps(request_content).encode("utf-8")
    # print("重新编码以后的数据：",request_data.decode("utf-8"))
    return request_data
