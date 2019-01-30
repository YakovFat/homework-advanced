import datetime
import time


class DaTi:

    def __enter__(self):
        now = datetime.datetime.now().time()
        start_time = time.time()
        self.start_time = start_time
        self.now = now
        print(now)

    def __exit__(self, type, value, traceback):
        old = datetime.datetime.now().time()
        self.old = old
        print(old)
        print(time.time() - self.start_time)


if __name__ == '__main__':
    with DaTi() as c:
        print('hello')
