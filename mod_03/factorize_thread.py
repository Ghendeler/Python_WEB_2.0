from threading import Thread
from time import time


def factorize(*number):
    res = []
    for num in number:
        thread = Factorize_Thread(args=(num,))
        thread.start()
        thread.join()
        res.append(thread.value)
    return res


class Factorize_Thread(Thread):

    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None, *, daemon=None) -> None:
        super().__init__(group, target, name, daemon=daemon)
        self.value = []
        self.args = args

    def run(self):
        for i in range(1, self.args[0] + 1):
            if self.args[0] % i == 0:
                self.value.append(i)


if __name__ == '__main__':

    timer = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(time() - timer)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158,
                 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212,
                 2662765, 5325530, 10651060]
