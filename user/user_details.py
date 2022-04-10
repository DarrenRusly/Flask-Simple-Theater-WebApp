class User:
    def __init__(self, id, name, password, cat):
        self.id = id
        self.username = name
        self.__password = password
        self.cat = cat
    
    def getPassword(self):
        return self.__password