import os
import hashlib
import sys
sys.path.append('..')
from util.config_parser import load_config


DEFAULT_SIGN_CONFIG = 'sign.conf'

def sha1(str):
    m = hashlib.sha1()
    m.update(str.encode('utf8'))
    return m.hexdigest()


def sign_params(accessId, accessKey, params):
    _str=''
    if isinstance(params, list):
        params = params[0]
    for key in sorted(params.keys()):
        _str = _str + key + str(params[key])
    _str += accessKey
    sign = sha1(_str).upper()
    return [{"appid": accessId, "sign": sign, "auth-type":0}, params]


def sign(params, section='default'):

    conf = load_config(DEFAULT_SIGN_CONFIG, section)
    # print(conf)
    accessId = conf.get('accessid')
    accessKey = conf.get('accesskey')
    # print(accessId, accessKey)
    return sign_params(accessId, accessKey, params)

if __name__ == '__main__':
    sign({"a":1}, "station")
