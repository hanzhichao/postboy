#!/bin/env/python
# coding=utf-8
from threading import Thread

class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.work_queue = None
        self.work_results = None

    def set_work_queue(self, work_queue):
        self.work_queue = work_queue

    def set_work_results(self, work_results):
        self.work_results = work_results

    def run(self):
        while(true):
            api = this.work_queue.pool()
            if not api:
                break
            response_list = self.post(api) 

    def post(self, api):
        