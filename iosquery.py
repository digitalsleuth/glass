'''
This python script contains sql commands to run on iOS devices.
The commands are organized by what they do.
'''
class Iosquery(object):

    def __init__(self):
        self.s1 = "SELECT ZNAME FROM ZMOEMPLOYER;"
        self.SELECT = [self.s1]
    
    def getSelect(self):
        return self.SELECT

query = Iosquery()
