#!/bin/env/python
# coding=utf-8
import os

# if '"code":100000' in res.text:
                #     print("%s ------ PASS" % api_file)
                # else:
                #     print("%s ------ FAIL" % api_file)



if os.path.isdir(sys.argv[1]):
    for root, dirs, files in os.walk(sys.argv[1], topdown=False):
        for name in files:
            if name[-5:] == '.json':
                # print(os.path.join(root, name))
                postboy.post(os.path.join(root, name))

elif os.path.isfile(sys.argv[1]):
    postboy.post(sys.argv[1])
else:
    print("文件不存在")