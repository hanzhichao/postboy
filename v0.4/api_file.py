import json
from api import Api

class ApiFile(object):
    def __init__(self):
        pass

    @staticmethod
    def load(api_file):
        with open(api_file, encoding='utf-8') as f:
            apis = json.load(f)
        apis = apis if isinstance(apis, list) else [apis]
        return map(lambda x:Api(x), apis)


if __name__ == "__main__":
    ApiFile.load("data/api/shop/shop_Istation_matchStation_POST.json")