import keyring
from quickstart import testKey
import schedule
import time


class Test:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def scheduled_print(self):
        print(f"HELLO, THIS IS TEST: {self.name}")


if __name__ == '__main__':

    testList = [1,2,3]

    for item in testList:
        testItem = Test(item)
        schedule.every(1).minutes.do(testItem.scheduled_print)

    while True:
        schedule.run_pending()
        time.sleep(1)
