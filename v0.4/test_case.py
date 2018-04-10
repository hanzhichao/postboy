"""测试用例，一条用例对应一个api json文件，一条用例可能包含多个Api,一个Api可能包含多个Request"""
from queue import Queue
import os
from api_file import ApiFile



class TestCase(object):
    def __init__(self, api_file):
        self.api_list = ApiFile.load(api_file)   # 返回 [Api object, Api object, ....]  Api object 包含 Request Concurrency Times Data等
        self.test_case_result = [] # 结果形式为 [[(1,api_path,PASS,0.23),(2,api_path,PASS, 0.22)],[(1,api_path, PASS, 0.33)]]
        self.name = "/".join(api_file.split(os.sep)[-3:])[:-5]

    def get_name(self):
        return self.name

    def submit(self):
        pass

    def run(self):
        for api in self.api_list:
            api.run()
            api_result = api.get_api_result()
        self.test_case_result.append((api.api.get('url'), api_result))

    def is_complete(self):
        pass

    def get_test_case_result(self):
        return self.test_case_result


if __name__ == "__main__":
    t = TestCase("data\\api\\shop\\shop_Istation_getGoodsCode_POST.json")
    t.run()
    print(t.get_test_case_result())