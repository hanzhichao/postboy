import os
import configparser


class Config(object):
    def __init__(self):
        self.PrPath = os.path.dirname(__file__)
        self.cf = configparser.ConfigParser()
        self.cf.read(os.path.join(self.PrPath, 'conf','test.conf'))

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DB", name)
        return value