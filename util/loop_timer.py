#!/bin/env/python
# coding=utf-8

from threading import Timer



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
