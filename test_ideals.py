import keyring
from quickstart import testKey
import schedule
import time
from abc import ABC, abstractmethod


class Test(ABC):
    @abstractmethod
    def test(self):
        pass

    def real(self, ls):
        print("Zub")
        print(ls)

class testChild(Test):

    TEST_LIST = [1,2,3]

    def test(self):
        return "hello"

    def another(self):
        self.real(self.TEST_LIST)




if __name__ == '__main__':
    t = testChild()

    t.another()
