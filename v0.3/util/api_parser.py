#!/bin/env/python
# coding=utf-8
import json
from .config_parser import load_config
from .json_parser import load_json
import requests
import os
from .sign_maker import sign_params
import logging
from functools import wraps
import time
import inspect



logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG) 
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

def exec_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        parent_action = inspect.stack()[1][4][0].strip()
        back = func(*args, **kwargs)
        _exec_time = time.time()-t0
        logger.debug(parent_action + '---' + func.__name__ + '---' + str("%.3fs" % _exec_time))
        return back
    return wrapper





@exec_time
def login():
    session = requests.Session()
    config = load_json(os.path.join(os.getcwd(), 'data/login.json'))
    res = session.post(config.get('url'), headers=config.get('headers'), data=config.get('data'))
    return session

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

@exec_time
def handle_data(api):
    data = api.get('data')

    format_data = api.get('format_data')
    if format_data:
        for key in api['data'].keys():
            if '%s' in api['data'][key]:
                data[key] = data[key] % json.dumps(api.get('_'+key))

    sign = api.get('sign')
    if sign:
        data = sign_params(sign.get('accessId'),sign.get('accessKey'),api['data'])

    # print(api.get('headers'))
    headers = api.get('headers')
    if headers and isinstance(headers, dict):
        for key in headers.keys():
            if key.lower() == 'content-type':
                if "json" in headers[key]:
                    data= json.dumps(data)
    return data

@exec_time
def format_api(api):
    api['session'] = handle_session(api)
    api['url'] = handle_url(api)
    api['headers'] = handle_headers(api)
    api['cookies'] = handle_cookies(api)
    api['data'] = handle_data(api)
    return api


if __name__ == '__main__':
    pass
