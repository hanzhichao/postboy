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
from threading import Thread
from threading import Timer
import os
from functools import wraps
from sign import sign_params


if (platform.python_version()) < '3':
    import codecs
    import ConfigParser
else:
    import configparser as ConfigParser
    from functools import reduce

current_threads = 0
rt = []
rt2 = []
t_num = []
tps = []
finished = False

def load_config(path, section='default'):
    if (platform.python_version()) < '3':
        conf = ConfigParser.ConfigParser()
        with open(path, encoding='utf-8') as f:
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
        with codes.open(path, encoding='utf-8') as f:
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

class LoopTimer(Timer):
    def __init__(self, interval, function, args=[], kwargs={}):  
        Timer.__init__(self,interval, function, args, kwargs)


    def run(self):  
        while not finished:  
            self.finished.wait(self.interval)  
            if self.finished.is_set():  
                self.finished.set()  
                break  
            self.function(*self.args, **self.kwargs)


def timer(seconds):
    def _timer(func): 
        def get_avarage():
            global rt
            global rt2
            global t_num
            global tps
            rt_length = len(rt)
            # print(rt_length)
            threads_num = math.ceil(math.sqrt(rt_length))
            # print(threads_num)

            if rt:
                rt_avarage = reduce(lambda x,y:x+y, rt) / len(rt)
                rt_min = min(rt)
                rt_max = max(rt)
                c_tps = threads_num / rt_avarage
            else:
                rt_avarage = 0
                rt_min = 0
                rt_max = 0
                tps = 0

            rt2.append(rt_avarage)
            tps.append(c_tps)
            t_num.append(threads_num)

            # print("平均相应时间：%.3fs, 最小相应时间：%.3fs, 最大相应时间：%.3fs, 当前并发：%.3f, 吞吐量：%.3f" % (rt_avarage, rt_min, rt_max, threads_num, tps))
            # print(len(rt))
            
        @wraps(func)
        def wrapper(*args, **kwargs):
            timer = LoopTimer(seconds, get_avarage)
            timer.start()
            return func(*args, **kwargs)
        return wrapper
    return _timer

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


def load_threads(init_threads, max_threads, increaced_threads, time_interval):
    def _threads(func):
        @wraps(func)
        def wrapper(*args, **kwargs):


            def get_avarage():
                global rt
                global tps
                rt_avarage = reduce(lambda x,y:x+y, rt) / len(rt)
                rt_min = min(rt)
                rt_max = max(rt)
                # print("平均相应时间：%.3fs, 最小相应时间：%.3fs, 最大相应时间：%.3fs" % (rt_avarage, rt_min, rt_max))


            def run_threads(threads_num, timeout=None):
                threads = []
                for i in range(threads_num):
                    if not args or kwargs:
                        t = Thread(target=func)
                    elif args:
                        t = Thread(target=func, args=args)
                    elif kwargs:
                        t = Thread(target=func, args=kwargs)
                    threads.append(t)
                for i in range(threads_num):
                    threads[i].start()
                
                global current_threads
                current_threads = threads_num

                for i in range(threads_num):
                    threads[i].join(timeout)

            start_time = time.time()
            # print("start:%s" % time.ctime())
            run_threads(init_threads)


            current_threads = init_threads
            while current_threads < max_threads:
                # print("-"*100)
                time.sleep(time_interval)
                if current_threads + increaced_threads < max_threads:
                    run_threads(current_threads + increaced_threads)
                else:
                    run_threads(current_threads + max_threads - current_threads)
                current_threads = current_threads + increaced_threads


            global finished
            finished = True  # stop the timer
            # print("程序总用时：%.3fs" % (time.time()-start_time))
            # print("end:%s" % time.ctime())
            return func
        return wrapper
    return _threads


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


def save_map():
    chart = Highchart()

    chart.set_options('chart', {'inverted': True})

    options = {
        'title': {
            'text': 'LoadBoy 接口负载图'
        },
        'subtitle': {
            'text': '响应时间/吞吐量/线程数'
        },
        'xAxis': {
            'reversed': False,
            'title': {
                'enabled': True,
                'text': '响应时间'
            },
            'labels': {
                'formatter': 'function () {\
                    return this.value + " t/s";\
                }'
            },
            'maxPadding': 0.05,
            'showLastLabel': True
        },
        'yAxis': {
            'title': {
                'text': '线程数'
            },
            'labels': {
                'formatter': "function () {\
                    return this.value + '';\
                }"
            },
            'lineWidth': 2
        },
        'legend': {
            'enabled': False
        },
        'tooltip': {
            'headerFormat': '<b>{series.name}</b><br/>',
            'pointFormat': ''
        }
    }

    chart.set_dict_options(options)

    global rt2
    global tps
    global t_num
    tps_data = list(zip(tps, t_num))
    chart.add_data_set(tps_data, 'spline', 'tps', marker={'enabled': False}) 

    rt_data = list(zip(rt2, t_num))
    chart.add_data_set(rt_data, 'line', 'rt', marker={'enabled': False}) 

    chart.save_file()




demo()
save_map()