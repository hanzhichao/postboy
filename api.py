"""格式化每段接口请求"""
import json
from http_request import HttpRequest
from auth import sign_params



class Api(object):
    def __init__(self, api):
        self.api = api
        self.concurrency = int(api.get('concurrency')) if api.get('concurrency') else 1
        self.times = int(api.get('times')) if api.get('times') else 1
        self.threads = self.set_threads()
        self.api_result = []

    def set_threads(self):
        threads = []
        for j in range(0, self.times//self.concurrency):
            for i in range(self.concurrency):
                t = self.new_http_request()
                threads.append(t)
        return threads

    def new_http_request(self):
        request = HttpRequest()
        request.set_url(self.api.get('url'))
        request.set_headers(self.api.get('headers') if self.api.get('headers') else \
            {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"})
        request.set_data(self.handle_data())
        return request


    def handle_data(self):
        # sign data
        is_sign = self.api.get('sign')
        if is_sign:
            if isinstance(is_sign, dict):
                data = sign_params(is_sign.get('accessId'), is_sign.get('accessKey'), self.api.get('data'))
            else:
                data = sign(data, is_sign)

        # headers
        headers = self.api.get('headers')
        if headers and isinstance(headers, dict):
            for key in headers.keys():
                if key.lower() == 'content-type':
                    if "json" in headers[key]:
                        data= json.dumps(data)
        return data

    def run(self):
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        for i in range(0,len(self.threads)):
            self.api_result.append((i+1,self.threads[i].get_request_result()))

    def get_api_result(self):
        return self.api_result



if __name__ == "__main__":
    a = Api({"url":"/api/Istation/matchStation","sign":{"accessId":"station","accessKey":"NTA3ZTU2ZWM5ZmVkYTVmMDBkMDM3YTBi"},"headers":{"Content-Type":"application/json;charset=utf-8"},"data":{"lng":"116.123","lat":"39.890358"}})
    print(a.concurrency, a.times)
    print(a.api.get('url'))
    print(a.threads)
    a.send()
    print(a.get_api_result())
