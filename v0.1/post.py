#!/bin/env/python
# coding=utf-8
"""饿了么/美团/百度外卖 三方平台 测试/预发环境切换器"""
import sys
import json
import requests
import platform
import hashlib
from threading import Thread
import os


if (platform.python_version()) < '3':
    import codecs
    import ConfigParser
else:
    import configparser as ConfigParser


def config(option, section='default', path=os.path.join(os.path.dirname(__file__), 'default.conf')):
    conf = ConfigParser.ConfigParser()
    conf.read(path)
    return conf.get(section, option)


def load(path):
    """加载json文件,:@param path: json文件路径,:return 字典格式"""
    if (platform.python_version()) < '3':
        with codes.open(path, encoding='utf-8') as f:
            return json.load(f)
    else:
        with open(path, encoding='utf-8') as f:
            return json.load(f)

def thread(func):
    def wrapper(*args, **kwargs):
        if not args or kwargs:
            t = Thread(target=func)
        elif args:
            t = Thread(target=func, args=args)
        elif kwargs:
            t = Thread(target=func, args=kwargs)
        t.start()
        return func
    return wrapper

# appId = "CORE0002"
# accessKey = "BMLYkAKNcAthZbW7kQDUe8i4PmLoek"

def sha1(str):
    m = hashlib.sha1()
    m.update(str.encode('utf8'))
    return m.hexdigest()


def get_session():
    session = requests.Session()
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    login_uri = "http://test.spicespirit.com/index/index/login"
    login_data = {"nickname": "hanzhichao", "password": "hanzhichao"}

    res = session.post(login_uri, headers=headers, data=login_data)
    return session


def sign_params(accessId, accessKey, params):

    str=''
    for key in sorted(params.keys()):
        str = str + key + params[key]
    str += accessKey
    sign = sha1(str).upper()
    return [{"appid": accessId, "sign": sign, "auth-type":0}, params]



def post(api_file, base_url=None):
    
    if api_file[-5:]!='.json':
        api_file = api_file + '.json'
    api = load(api_file)


    if not api.get('url'):
        if not base_url:
            base_url = config('base_url')
        api_url = base_url + api['uri']
    else:
        api_url = api.get('url')

    # need sign or not
    if api.get('sign'):
        sign = api.get('sign')
    else:
        sign = json.loads(config('sign'))

    if sign:
        accessId = sign.get('accessId')
        accessKey = sign.get('accessKey')
        data = sign_params(accessId,accessKey,api['data'])
    else:
        data = api['data']

    # headers
    if api.get('headers'):
        headers = api.get('headers')
    else:
        headers = json.loads(config('headers'))
    if "application/json" in headers.get('Content-Type'):  # must be Content-Type
        data = json.dumps(data)


    # if is login_required
    if api.get('login_required') is not None:
        login_required = api.get('login_required')
    else:
        login_required = False if config('login_required')=='False' else True

    if login_required:
        session = get_session()
    else:
        session = requests.Session()

    # post request
    res = session.post(api_url, headers=headers, data=data)

    # assert response
    if api.get('assert'):
        _assert = api.get('assert')
    else:
        _assert = config('assert')

    if _assert:

        try:
            assert(_assert in res.text)
            print(res.text)
            # print(json.dumps(res.json(), ensure_ascii=False, indent=2))
            # print("%s ------ PASS" % api_file)
        except AssertionError:
            print(res.text)
            # print(json.dumps(res.json(), ensure_ascii=False, indent=2))
            # print("%s ------ Fail" % api_file[:-5])
    else:
        print(res.text)
        # print(json.dumps(res.json(), ensure_ascii=False, indent=2))

def main():
    if len(sys.argv) > 1:
        # print(len(sys.argv))
        post(sys.argv[1]) 

# if __name__ != '__main__':
main()
# post('api/user/getInfoById') 
# post('api/getGoodsCode.json', 'http://detail.spicespirit.com') 