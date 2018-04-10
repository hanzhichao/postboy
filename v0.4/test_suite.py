from test_case import TestCase
from config import Config
import os
local_config = Config()

class TestSuite():
    def __init__(self):
        self.test_suite = []
        self.test_suite_result = []


    def add_case(self, test_case):
        self.test_suite.append(test_case)


    def add_api_file_as_case(self, api_file):
        self.test_suite.append(TestCase(api_file))


    def run(self):
        for test_case in self.test_suite:
            test_case.run()
            self.test_suite_result.append((test_case.name,test_case.get_test_case_result()))

    def get_test_suite_result(self):
        return self.test_suite_result
     

if __name__ == "__main__":
    t = TestSuite()
    # print(t.test_suite)
    # t.test_suite[0].run()
    t.run()
    # print(t.discover())
    print(t.get_test_suite_result())