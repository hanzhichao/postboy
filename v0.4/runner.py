import os
from test_suite import TestSuite
from test_case import TestCase
from report import Report


class Runner(object):
    def __init__(self):
        pass

    def discover(self, path):
        test_suite = TestSuite()
        for api_file in self.collect(path):
            test_case = TestCase(api_file)
            test_suite.add_case(test_case)
        return test_suite

    def collect(self, path):
        api_file_list = []
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    if name.endswith('.json'):
                        api_file_list.append(os.path.join(root, name))   # 只适用于相对路径
        elif os.path.isfile(self.path):
            api_file_list.append(path)
        else:
            print("文件不存在")
        return api_file_list

    def add_api_file(self, api_file):
        self.api_file_list.append(api_file)


    def set_test_suite(self):
        for api_file in self.api_file_list:
            test_case = TestCase(api_file)
            self.test_suite.add_case(test_case)

if __name__ == "__main__":
    r = Runner()
    t = r.discover("data\\api\\shop\\")
    t.run()
    results = t.get_test_suite_result()
    report = Report(results).save("report.html")
    
