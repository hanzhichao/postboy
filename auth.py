import hashlib
import json
import re

def sha1(str):
    m = hashlib.sha1()
    m.update(str.encode('utf8'))
    return m.hexdigest()


def signMaker(accessId, accessKey, params):
    str = re.sub('[\{\}\"\':, ]','',json.dumps(params, sort_keys=True, ensure_ascii=False)) + accessKey
    sign = sha1(str).upper()
    # print(params)
    # print(str)
    # print(sign)
    return [{"appid": accessId, "sign": sign, "auth-type":0}, params]

