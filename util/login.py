#!/bin/env/python
# coding=utf-8

import os
import requests
import sys
sys.path.append('..')
from util.json_parser import load_json


def login():
    session = requests.Session()
    login_api = load_json(os.path.join(os.getcwd(), 'api/login.json'))
    res = session.post(login_api.get('url'), headers=login_api.get('headers'), data=login_api.get('data'))
    return session
