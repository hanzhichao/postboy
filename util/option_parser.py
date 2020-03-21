#!/usr/bin/env python
"""add command options for mini_spider.py"""
# -*- coding: utf-8 -*-
import optparse


# comand option parser for mini_spider.py
parser = optparse.OptionParser()
parser.add_option("-c", "--conf",
                  action="store",
                  dest="conf",
                  help="load config file",
                  metavar="FILE")
parser.add_option("-v", "--version",
                  action="store_true",
                  dest="version",
                  help="show project version")
(options, args) = parser.parse_args()
