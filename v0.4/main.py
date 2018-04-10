from random import random

from master import Master
from task import Task
import time

class Main(object):
    def __init__(self):
        master = Master(20)
        for i in range(1, 101):
            t = Task()
            t.setId(i)
            t.setName("任务" + str(i))
            t.setPrice(random()*1000)
            master.submit(t)
        master.execute()

        start = time.time()
        res = master.get_results()
        
        while True:
            if master.is_complete():
                end = time.time() - start
                print(master.get_results())
                break




if __name__ == '__main__':
    m = Main()