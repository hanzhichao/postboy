#!/bin/env/python
# coding=utf-8

import os



# handle data file
def  data_generator(data_file, sep=","):
    data_file_path = os.path.join(os.path.dirname(__file__), "../data/" + data_file)
    with open(data_file_path) as f:
        lis = [x.strip().split(sep) for x in f ]
        # print(lis)

    i = 0
    while True:
        if i >= len(lis):
            i = 0
        yield(lis[i])
        i = i + 1

    

if __name__ == '__main__':
    a = data_generator("data.txt", 0)
    print(next(a))
    print(next(a))
    print(next(a))
    print(next(a))
    print(next(a))














