#!/bin/env/python
# coding=utf-8
"""饿了么/美团/百度外卖 三方平台 测试/预发环境切换器"""
import sys
import json
import requests
import platform
import time
import random
import math

from highcharts import Highchart


import os

from sign import sign_params



current_threads = 0
rt = []
rt2 = []
t_num = []
tps = []
finished = False




# def get_avarage(seconds=1):
    # def _get_avarage():
    #     global rt
    #     global tps
    #     rt_avarage = reduce(lambda x,y:x+y, rt) / len(rt)
    #     rt_min = min(rt)
    #     rt_max = max(rt)
    #     print("平均相应时间：%.3fs, 最小相应时间：%.3fs, 最大相应时间：%.3fs" % (rt_avarage, rt_min, rt_max))

    # timer = LoopTimer(seconds, _get_avarage)
    # timer.start()





@timer(1)
@load_threads(1, 100, 5, 0)
def demo():
    start_time = time.time()
    api = {"url":"http://192.168.100.238:8089/api/Istation/matchStation","sign":{"accessId":"CORE0002","accessKey":"BMLYkAKNcAthZbW7kQDUe8i4PmLoek"},"data":{"lng":"116.334223","lat":"39.975377"}}

    headers={"Content-Type": "application/json"}
    data = sign_params(api['sign']['accessId'], api['sign']['accessKey'], api['data'])
    # print(data)

    res=requests.post(url=api['url'], headers=headers, data=json.dumps(data))
    # print(res.text)
    rt.append(time.time()-start_time)
    # print(len(rt))
    # print(current_threads)
    # print("接口相应时间：%.3fs" % (time.time()-start_time))

# RT = 
# timer = LoopTimer(1, get_avarage)
# timer.start()






demo()
save_map()