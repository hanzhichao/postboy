#!/bin/env/python
# coding=utf-8
import platform


if (platform.python_version()) < '3':
    import codecs
    import ConfigParser
else:
    import configparser as ConfigParser


def load_config(path, section='default'):
    if (platform.python_version()) < '3':
        conf = ConfigParser.ConfigParser()
        with codecs.open(path, encoding='utf-8-sig') as f:
            conf.readfp(f)
    else:
        conf = ConfigParser.RawConfigParser()
        conf.read(path, encoding='utf8')

    _dict = {}
    for option in conf.options(section):
        _dict[option] = conf.get(section, option)
    return _dict

