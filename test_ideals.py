import keyring
from quickstart import testKey
import schedule
import time
from abc import ABC, abstractmethod
from datetime import date, datetime


class Test(ABC):

    def __init__(self):
        self.testThing = {}

    @abstractmethod
    def test(self):
        pass

    def real(self, ls):
        self.testThing["123"] = "HELLO"

class testChild(Test):

    TEST_LIST = [1,2,3]

    def test(self):
        self.testThing['GO'] = 'ZUUB'

    def another(self):
        self.real(self.TEST_LIST)
        print(self.testThing)


if __name__ == '__main__':
    today = date.today()
    testDate = datetime.strptime('Wed, Jan 25, 2023', '%a, %b %d, %Y').date()

    timeDelta = today - testDate

    print(f"Days: {timeDelta.days} and type: {type(timeDelta)}")

