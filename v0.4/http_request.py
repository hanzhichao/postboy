import requests
from config import Config
from threading import Thread
import time
local_config = Config()


class HttpRequest(Thread):
    def __init__(self):
        Thread.__init__(self)
        global host, port, timeout
        host = local_config.get_http("base_url")
        port = local_config.get_http("port")
        timeout = local_config.get_http("timeout")
        self.method = 'POST'
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.response = None

    def set_method(self, method):
        self.method = method

    def set_url(self, url):
        self.url = host + ":" + port + url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, file):
        self.files = file

    def set_work_queue(self, work_queue):
        self.work_queue = work_queue

    def set_work_results(self, work_results):   #包含用例名，执行结果，时间等
        self.work_results = work_results

    def run(self):
        if self.method.upper() == 'GET':
            try:
                response = requests.get(self.url, params=self.params, headers = self.headers, timeout=float(timeout))
                self.response = response
            except TimeoutError:
                # self.logger.error("Time out!")
                pass
        elif self.method.upper() == 'POST':
            try:
                response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,timeout=float(timeout))
                self.response = response
            except TimeoutError:
                # self.logger.error("Time out!")
                pass

    def get_response(self):
        return self.response.text

    def get_request_result(self):
        try:
            if self.response.status_code == 200:
                return "PASS"
            else:
                return "FAIL"
        except Exception as e:
            print(self.url, self.headers, self.data)
            print(self.response)
            # print(e)
            return "ERROR"

if __name__ == "__main__":
    h = HttpRequest()
    h.set_url("/api/Istation/matchStation")
    h.set_headers({"Content-Type": "application/json;charset=utf-8"})
    h.set_data({"lng": "116.123","lat": "39.890358"})
    h.start()
    h.join()
    print(h.get_response())
    print(h.get_request_result())