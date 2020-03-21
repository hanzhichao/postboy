#!/bin/env/python
# coding=utf-8

import sys
import requests
import time
import os
# sys.path.append('..')
from util.sign_maker import sign_params
from util.config_parser import load_config
from util.json_parser import load_json
from threading import Thread
from functools import wraps
import json
from util.api_parser import format_api
from util.api_parser import exec_time



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
    def __init__(self, config_file=os.path.join(os.getcwd(), 'conf/default.conf')):
        self.config = load_config(config_file)
   
    @exec_time
    def mix_api(self, api_file):
        api_list = []
        config = self.config.copy()
        # config = load_config(self.config_file)
        for api in list(load_json(api_file)):
            config.update(api)
            formatted_api = format_api(config)
            api_list.append(formatted_api)

        return api_list

    @exec_time
    @threads
    def post(self, api):
        # print(api)
        method = api.get('method')
        if not method or method.upper() == 'POST':
            start_time = time.time()
            session = api.get('session')
            url = api.get('url')
            headers = api.get('headers')
            cookies = api.get('cookies')
            data = api.get('data')

            res = session.post(url, headers=headers, cookies=cookies, data=data)

            print(json.dumps(res.json(), ensure_ascii=False)),
            print("--- %.3fs" % (time.time()-start_time))
            # print(json.dumps(res.json(), ensure_ascii=False, indent=2))     # to handle ISO-8895-1


    def send_request(self, api_file):
        for api in self.mix_api(api_file):         
            self.post(api) 
                                                

# def main():
#     if len(sys.argv) > 1:
#         # print(sys.argv[1])                           

#         postboy.post(sys.argv[1])
    

# # if __name__ != '__main__':
# main()
# post('api/user/getInfoById') 
# post('api/getGoodsCode.json', 'http://detail.spicespirit.com') 

# print(load_json("D:\Projects\postboy\api\Istation\matchStation.json"))
postboy = PostBoy()
postboy.send_request("data/api/shop/matchStation.json")
# postboy.read_api("D:\Projects\postboy\api\Istation\matchStation.json")
# print(postboy.params)