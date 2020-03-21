
class  Task(object):
    def __init__(self):
        self.id = 0
        self.name = ''
        self.price = 0.00

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getPrice(self):
        return self.price

    def setPrice(self, price):
        self.price = price