#!/bin/env/python
# coding=utf-8
import sys
import json
import requests
import platform
import time

from threading import Thread
import os
from functools import wraps
# from sign import sign_params
from auth import signMaker

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
# import chardet
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码


if (platform.python_version()) < '3':
    import codecs
    import ConfigParser
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    import configparser as ConfigParser


def load_config(path, section='default'):
    if (platform.python_version()) < '3':
        conf = ConfigParser.ConfigParser()
        with codecs.open(path, encoding='utf-8') as f:
            conf.readfp(f)
    else:
        conf = ConfigParser.RawConfigParser()
        conf.read(path, encoding='utf8')

    _dict = {}
    for option in conf.options(section):
        _dict[option] = conf.get(section, option)
    return _dict


def load_json(path):
    """加载json文件,:param path: json文件路径 :return 字典格式"""
    if (platform.python_version()) < '3':
        with codecs.open(path, encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                print("%s --- json decode error" % path)

    else:
        with open(path, encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                print("%s --- json decode error" % path)


def login():   #  login.json中配的域名是test.spicespirit.com   api_file中的域名不一致时cookies不生效
    session = requests.Session()
    config = load_json(os.path.join(os.path.dirname(__file__), 'login.json'))
    res = session.post(config.get('url'), headers=config.get('headers'), data=config.get('data'))
    return session

def _show_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("start %s ... ..." % func.__name__)
        start_time = time.time()
        func_result = func(*args, **kwargs)
        print("%s 执行时间：%.3fs" % (func.__name__, time.time()-start_time))
        return func_result
    return wrapper


def threads(concurrency, times):
    def _threads(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # print("start:%s" % time.ctime())
            for i in range(0, times//concurrency):
                threads = []
                for i in range(concurrency):
                    if not args or kwargs:
                        t = Thread(target=func)
                    elif args:
                        t = Thread(target=func, args=args)
                    elif kwargs:
                        t = Thread(target=func, args=kwargs)
                    threads.append(t)
                for i in range(concurrency):
                    threads[i].start()
                for i in range(concurrency):
                    threads[i].join()
            # print("end:%s" % time.ctime())
            return func
        return wrapper
    return _threads


class PostBoy(object):
    def __init__(self, config_file=os.path.join(os.path.dirname(__file__), 'default.conf')):
        self.config = load_config(config_file)
        self.body_list = []
        # self.file_data = {}
        # self.data_index = 0


    def read_api(self, api_file):
        api_list = []
        params = {}
        api = load_json(api_file)
        if isinstance(api, dict):
            api_list.append(api)
        if isinstance(api, list):
            api_list = api

        for api in api_list:
            if not api.get('url'):  # todo try ... except ...
                if not base_url:
                    base_url = self.config.get('base_url')
                params['api_url'] = base_url + api['uri']
            else:
                params['api_url'] = api.get('url')

            # format data
            if api.get('format_data') is True:
                for key in api['data'].keys():
                    if '%s' in api['data'][key]:
                        api['data'][key] = api['data'][key] % json.dumps(api.get('_'+key))
            


            # need sign or not
            if api.get('sign'):
                sign = api.get('sign')
            else:
                sign = json.loads(self.config.get('sign'))

            if sign:
                accessId = sign.get('accessId')
                accessKey = sign.get('accessKey')
                params['data'] = signMaker(accessId,accessKey,api['data'])
            else:
                params['data'] = api['data']

            # headers
            if api.get('headers'):
                headers = api.get('headers')
            else:
                headers = json.loads(self.config.get('headers'))
            if "application/json" in headers.get('Content-Type'):  # must be Content-Type
                params['data'] = json.dumps(params['data'])

            # if is login_required
            if api.get('login_required') is not None:
                params['login_required'] = api.get('login_required')
            else:
                params['login_required'] = False if self.config.get('login_required')=='False' else True



            # handle cookies
            if api.get('cookies'):
                params['cookies'] = api.get('cookies')


            # handle concurrency and times
            if api.get('concurrency') and api.get('times'):
                params['concurrency'] = int(api.get('concurrency'))
                params['times'] = int(api.get('times'))
            else:
                params['concurrency'] = int(self.config.get('concurrency'))
                params['times'] = int(self.config.get('concurrency'))

            self.body_list.append(params)


    # def change_data(self):
    #     for i in range(0, len(self.body_list)):
    #         for key in self.file_data.keys():
    #             first = self.file_data[key][0]
    #             print(self.body_list,i,first,type(self.body_list[i]))
                # self.body_list[i]['data'][key] = first
                # api['data'][key] = first
                # self.file_data[key].append(first)
                # self.file_data[key].pop(0)


    def post(self, api_file):
        self.read_api(api_file)
        for params in self.body_list:
            @threads(params.get('concurrency'), params.get('times'))
            def _post():
                if params.get('login_required'):
                    session = login()
                else:
                    session = requests.Session()
                
                # post request
                # print(params)
                res = session.post(params.get('api_url'), 
                    headers=params.get('headers'), 
                    cookies=params.get('cookies'), 
                    data=params.get('data'))

                # try:
                #     print(json.dumps(res.json(), ensure_ascii=False, indent=2))
                # except json.decoder.JSONDecodeError:  # only python3
                #     try:
                #         print(res.text)
                #     except UnicodeEncodeError:
                #         html = res.content
                #         html_doc=html.decode("utf-8","ignore").replace('\xa9', '')
                #         print(html_doc)

                # print(json.dumps(res.json(), indent=2))

                # print(res.text)  # [Decode error - output not utf-8]
                if res.status_code == 200:
                    print("%s ------ PASS" % api_file)
                else:
                    print("%s ------ FAIL" % api_file)

            _post()
                                                

def main():
    results = []
    if len(sys.argv) > 1:
        # print(sys.argv[1])                           
        # postboy = PostBoy()
        if os.path.isdir(sys.argv[1]):
            for root, dirs, files in os.walk(sys.argv[1], topdown=False):
                for name in files:
                    if name[-5:] == '.json':
                        # print(os.path.join(root, name))
                        postboy = PostBoy()
                        postboy.post(os.path.join(root, name))

        elif os.path.isfile(sys.argv[1]):
            postboy = PostBoy()
            postboy.post(sys.argv[1])
        else:
            print("文件不存在")
    

# if __name__ != '__main__':
main()
# post('api/user/getInfoById') 
# post('api/getGoodsCode.json', 'http://detail.spicespirit.com') 

# print(load_json("D:\Projects\postboy\api\Istation\matchStation.json"))
# postboy = PostBoy()
# postboy.read_api("D:/Projects/postboy/v0.4/data/api/shop/matchStation.json")
# print(postboy.body_list[0]['data'])
# print(postboy.file_data)
# postboy.change_data()
# postboy.read_api("D:/Projects/postboy/v0.4/data/api/shop/matchStation.json")
# print(postboy.body_list)
# print(postboy.file_data)
# postboy.read_api("D:/Projects/postboy/v0.4/data/api/shop/matchStation.json")
# print(postboy.body_list)