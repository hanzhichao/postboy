#!/bin/env/python
# coding=utf-8
from threading import Thread

class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.work_queue = None
        self.work_results = {}

    def set_work_queue(self, work_queue):
        self.work_queue = work_queue

    def set_work_results(self, work_results):
        self.work_results = work_results

    def run(self):
        while not self.work_queue.empty():
            task = self.work_queue.get()
            print("任务id：" + str(task.getId()) + ", name: " + task.getName() + ", price: " + str(task.getPrice()))
            self.work_results[str(task.getId())] = "OK"


if __name__ == "__main__":
    w = Worker()
    w.start()
