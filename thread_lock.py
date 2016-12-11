from multiprocessing import Process, Lock
import time


def processData(thread_mutex, data):
    with thread_mutex:
        time.sleep(1)
        print('Do some stuff')


if __name__ == '__main__':
    thread_mutex = Lock()
    for i in range(10):
        p = Process(target = processData, args = (thread_mutex, 'hello'))
        p.start()