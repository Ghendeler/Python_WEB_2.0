from multiprocessing import Process, Pipe, cpu_count
from time import time


# cpu_count() из пакета multiprocessing

def factorize(*number):
    res = []
    for num in number:
        conn1, conn2 = Pipe()
        process = Factorize_Process(args=(conn2,))
        process.start()
        conn1.send(num)
        answ = conn1.recv()
        res.append(answ)
    return res


class Factorize_Process(Process):
    def __init__(self, args=()):
        super().__init__()
        self.args = args
        self.conn = args[0]
        self.value = []

    def run(self) -> None:
        num = self.conn.recv()
        for i in range(1, num + 1):
            if num % i == 0:
                self.value.append(i)
        self.conn.send(self.value)


if __name__ == '__main__':

    print(cpu_count())

    timer = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(time() - timer)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158,
                 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212,
                 2662765, 5325530, 10651060]
