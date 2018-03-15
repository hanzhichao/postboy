import hashlib


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