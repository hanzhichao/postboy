#!/bin/env/python
# coding=utf-8
import Queue

class Master(object):

    # 4.构造方法
    def __init__(self, int worker_num):
        # 1.应该有个承装任务的集合
        self.work_queue = Queue.Queue(maxsize=0)

        # 2.是你用HashMap去承装所有worker对象
        self.workers = {}

        # 3.使用一个容器承装每一个worker执行任务的结果集合
        self.work_results = {}
        worker.set_work_queue(this.work_queue)
        worker.set_work_results(this.work_results)
    
    # 5. 提交方法
    def submit(task):
        this.work_queue.add(task)

    # 6.需要一个执行的方法
    def execute():
        for worker in self.workers:
            worker.start()

    # 7.判断所有线程是否执行完毕
    def is_complete():
        for worker in self.workers:
            if worker.is_alive():
                return False
            return True
        return False
    
    # 8.返回结果集
    def get_results():
        int ret
        for result in self.work_results:
           ret += int(result)
        return ret


