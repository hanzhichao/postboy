#!/bin/env/python
# coding=utf-8
from threading import Thread
from functools import wraps

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