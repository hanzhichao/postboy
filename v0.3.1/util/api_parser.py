#!/bin/env/python
# coding=utf-8
import json
import requests
import time
import copy
import re
import sys
import logging
from functools import wraps

sys.path.append('..')

from util.config_parser import load_config
from util.json_parser import load_json
from util.sign_maker import sign, sign_params
from util.login import login
from util.data_generator import data_generator


logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG) 
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def exec_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        back = func(*args, **kwargs)
        print(func.__name__ + " --- " + str(time.time()-t0) + "s")
        return back
    return wrapper

@exec_time
def handle_session(api):
    if api.get('login_required'):
        return login()
    else:
        return requests.Session()

@exec_time
def handle_url(api):
    url = api.get('url')
    if not url:
        base_url = api.get('base_url')
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        uri = api.get('uri')
        if uri[0] != '/':
            uri += '/'
        url = base_url + uri
    return url   # 可能为空或不合法

@exec_time
def handle_headers(api):
    headers = api.get('headers')
    if headers:
        if isinstance(headers, dict):
            return headers
        else:
            try:
                return json.loads(api.get('headers'))
            except TypeError:
                print("headers格式不正确")
                print(type(headers), headers)
    else:
        return {}

@exec_time
def handle_cookies(api):
    cookies = api.get('cookies')
    if cookies:
        if isinstance(cookies, dict):
            return cookies
        else:
            try:
                return json.loads(api.get('cookies'))
            except TypeError:
                print("cookies格式不正确")
                print(type(cookies), cookies)
    else:
        return {}


# must before handle data
@exec_time
def handle_source(apis):
    sources = {}
    for api in apis:
        source = api.get('source')
        if source:
            if isinstance(source, dict):
                for key in source.keys():
                    sources[key] = data_generator(source[key])
            else:
                print("source参数类型错误, 应为dict类型")
    return sources

@exec_time
def handle_data(api, sources):
    data = copy.deepcopy(api).get('data')

    # replace %s
    for key in data.keys():
        if '%s' in data[key]:
            data[key] = data[key] % json.dumps(api.get('_'+key))

        if data[key][:2] == '${' and  data[key][-1] == '}':
            _param = data[key][2:-1]
            if '[' not in _param or ']' not in _param:
                _param = _param + '[0]'

            _param_key = _param.split('[')[0]
            _param_index = int(_param.split('[')[1][:-1])
            data[key] = next(sources[_param_key])[_param_index]   # exception

    # sign data
    is_sign = api.get('sign')
    if is_sign:
        if isinstance(is_sign, dict):
            data = sign_params(is_sign.get('accessId'), is_sign.get('accessKey'), api['data'])
        else:
            data = sign(data, is_sign)

    # headers
    headers = api.get('headers')
    if headers and isinstance(headers, dict):
        for key in headers.keys():
            if key.lower() == 'content-type':
                if "json" in headers[key]:
                    data= json.dumps(data)
    return data


@exec_time
def handle_response(res, api):
    store_response = api.get('store_response')
    if store_response and isinstance(store_response, dict):
        for key in store_response.keys():
            regax = r'\{\{(.*)\}\}'
            match_results = re.findall(regax, store_response[key])
            if match_results:
                store_response[key] = res.get(match_results[0].strip())
    print(store_response)


# 要求api是原来的api
@exec_time
def format_api(api, sources):
    api = copy.deepcopy(api)
    api['session'] = handle_session(api)
    api['url'] = handle_url(api)
    api['headers'] = handle_headers(api)
    api['cookies'] = handle_cookies(api)
    api['data'] = handle_data(api, sources)
    return api


if __name__ == '__main__':
    api = {"url":"http://192.168.100.238:8089/api/Istation/matchStation","source":{"data1":"data.txt","data2":"data.txt"},"sign":"station","data":{"lng":"${data1[0]}","lat":"${data2[1]}"},"store_response":{"code":"{{ code }}"}}
    sources = handle_source([api])
    print(format_api(api, sources))
    # print(api)
    # print(format_api(api, sources))
    # print(format_api(api, sources))
