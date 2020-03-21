#!/bin/env/python
# coding=utf-8
import os
import platform


if (platform.python_version()) < '3':
    import codecs
    import ConfigParser
else:
    import configparser as ConfigParser


def load_config(path, section='default'):
    path = os.path.join(os.path.dirname(__file__), '../conf/' + path)
    # print(path)
    if (platform.python_version()) < '3':
        conf = ConfigParser.ConfigParser()
        with codecs.open(path, encoding='utf-8-sig') as f:
            conf.readfp(f)
    else:
        conf = ConfigParser.RawConfigParser()
        conf.read(path, encoding='utf8')

    _dict = {}
    for option in conf.options(section):    # 会都改为小写字母
        _dict[option] = conf.get(section, option)
    # print(_dict)
    return _dict

if __name__ == '__main__':
    print(load_config('sign.conf', 'station'))
