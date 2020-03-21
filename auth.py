import hashlib
import hmac
import requests


def login(base_url, username, password):
    session = requests.session()
    session.post(url='%s/index/index/login' % base_url, data={"nickname": username, "password": password})
    return session


def sign_service(access_id, access_key, params):
    def _sha1(str):
        m = hashlib.sha1()
        m.update(str.encode('utf8'))
        return m.hexdigest()

    def _link(params):
        if isinstance(params, dict):
            params = [params]

        _str = ''
        for param in params:
            for k in sorted(param.keys()):
                v = param[k]
                _str = _str + _sort(v) if isinstance(v, dict) or isinstance(v, list) else _str + k + str(v)
        return _str

    sign = _sha1(_link(params) + access_key).upper()
    return [{"appid": access_id, "sign": sign, "auth-type":0}, params]


def sign_third_logistics(access_key,params):
    def _hmac(accessKey,params):
        return hmac.new(accessKey.encode('utf8'), params.encode('utf8')).hexdigest()

    def _sort(params):
        if isinstance(params, dict):
            params = [params]

        _str = ''
        for param in params:
            for k in sorted(param.keys()):
                v = param[k]
                if not isinstance(v, dict) and not isinstance(v, list):
                    _str += str(v)
                else:
                    _str += _sort(v)
        return _str
    sort_params = _sort(params)
    params['sign'] = _hmac(access_key, sort_params)
    return params


if __name__ == '__main__':
    # login("http://test.spicespirit.com", "hanzhichao", "hanzhichao")
    # print(sign_service("station", "123", {"lng": "124", "lat": "234"}))
    print(sign_third_logistics("123", {"lng": "124", "lat": "234"}))
