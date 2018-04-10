#!/bin/env/python
# coding=utf-8
import sys
import requests
import time
import os
import json
import copy
from threading import Thread
from functools import wraps

from util.sign_maker import sign_params
from util.config_parser import load_config
from util.json_parser import load_json
from util.api_parser import format_api, handle_source, exec_time


def threads(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print("start:%s" % time.ctime())
        # print(args)
        # print(kwargs)
        concurrency = args[1].get('concurrency')
        times = args[1].get('times')
        
        if not concurrency:
            concurrency = 1
        else:
            concurrency = int(concurrency)
        if not times:
            times = 1
        else:
            times = int(times)

        # if not concurrency:
        #     concurrency = 1
        # else:
        #     try:
        #         concurrency = int(concurrency)
        #     except TypeError:
        #         print("concurrency数据格式错误")
        # if not times:
        #     times = 1
        # else:
        #     try:
        #         times = int(times)
        #     except TypeError:
        #         print("times数据格式错误")

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


class PostBoy(object):
    @exec_time
    def __init__(self, api_file, config_file='default.conf'):
        self.api_file = api_file
        self.config = load_config(config_file)
        apis = load_json(api_file)
        self.apis = apis if isinstance(apis, list) else [apis]
        self.apis = self.mix_apis()
        self.sources = handle_source(self.apis)
        if os.path.basename(api_file)[0:4].lower() == 'test':
            self.mode = 'Test'
        else:
            self.mode = 'Debug'
        print(self.mode)

    @exec_time
    def mix_apis(self):
        config = copy.deepcopy(self.config)
        func = lambda x:config if config.update(x) else config
        return list(map(func, self.apis))

    @exec_time
    def update_data(self, api):
        return format_api(api, self.sources)



    @threads
    def post(self, api):

        method = api.get('method')
        if not method or method.upper() == 'POST':
            start_time = time.time()

            session = api.get('session')
            url = api.get('url')
            headers = api.get('headers')
            cookies = api.get('cookies')
            data = api.get('data')
            @exec_time
            def _post():
                res = session.post(url, headers=headers, cookies=cookies, data=data)
                return res

            res = _post()
            if self.mode == 'Debug':
                print(data)
                print(json.dumps(res.json(), ensure_ascii=False))
                print("--- %.3fs" % (time.time()-start_time))
            else:
                print(res.text)
                if '"code":100000' in res.text:
                    print("%s ------ PASS" % self.api_file)
                else:
                    print("%s ------ FAIL" % self.api_file)
            # print(json.dumps(res.json(), ensure_ascii=False, indent=2))     # to handle ISO-8895-1


    def send_request(self):
        for api in self.apis:
            self.post(self.update_data(api))
                  

# def main():
#     if len(sys.argv) > 1:
#         # print(sys.argv[1])                           

#         postboy.post(sys.argv[1])
    

if __name__ == '__main__':
    # main()
    # post('api/user/getInfoById') 
    # post('api/getGoodsCode.json', 'http://detail.spicespirit.com') 

    pb = PostBoy("api/shop/test_matchStation.json")
    pb.send_request()
