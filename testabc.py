from abc import ABCMeta, abstractmethod, ABC

from PyQt6.QtCore import QThread, pyqtSignal

class Meta(type(ABC), type(QThread)):
    pass

class XXAstract(ABC,QThread,metaclass=Meta):

    @abstractmethod
    def testa(self):
        print("abstractmethod")
        pass

    def test(self):
        self.testa()

class yy():
    
    def testB(self):
        print("xxb")
        


class XX(XXAstract,yy):

    def testa(self):
        super().testa()
        print("xx")
        self.testB()


a = XX()
a.test()
