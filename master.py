#!/bin/env/python
# coding=utf-8
# import Queue
from queue import Queue
from worker import Worker


class Master(object):

    # 4.构造方法
    def __init__(self, num):
        # 1.应该有个承装任务的集合
        self.work_queue = Queue(maxsize=0)

        # 2.是你用HashMap去承装所有worker对象
        self.workers = {}

        # 3.使用一个容器承装每一个worker执行任务的结果集合
        self.work_results = {}

        for i in range(0, num):
            worker = Worker()
            worker.set_work_queue(self.work_queue)
            worker.set_work_results(self.work_results)
            self.workers["子节点"+str(i)] = worker

    # 5. 提交方法
    def submit(self, task):
        self.work_queue.put(task)

    # 6.需要一个执行的方法
    def execute(self):
        for key in self.workers:
            self.workers[key].start()


    # 7.判断所有线程是否执行完毕
    def is_complete(self):
        for key in self.workers.keys():
            if self.workers[key].isAlive():
                return False
            return True
        return False
    
    # 8.返回结果集
    def get_results(self):
        return self.work_results


