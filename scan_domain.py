import os
import sys
import subprocess
import time
import re
import threading

gUncheckDomainFile = 'UncheckDomain.txt'
gNotOccupiedFile = 'NotOccupied.txt'
gAlreadyOccupiedFile = 'AlreadyOccupied.txt'


class ScanDomain:
    def __init__(self):
        self.set_not_occupied_file = 'NotOccupied.txt'
        self.set_already_occupied_file = 'AlreadyOccupied.txt'
        self.set_thread_cnt = 20
        self.not_occupied_fd = None
        self.already_occupied_fd = None
        self.set_uncheck_domain_file = 'UncheckDomain.txt'
        self.lock = threading.Lock()
        self.uncheck_domain_list = list()

        self.quit = False
        self.running_thread_cnt = 0
        self.do_init()
        time.sleep(3)
        pass

    def do_init(self):
        self.already_occupied_fd = open(self.set_already_occupied_file, 'a+')
        self.not_occupied_fd = open(self.set_not_occupied_file, 'a+')
        self.get_domain()
        pass

    def add_not_occupied_domain(self, domain):
        self.lock.acquire()
        self.not_occupied_fd.write(domain + '\n')
        self.not_occupied_fd.flush()
        self.lock.release()
        pass

    def add_already_occupied_domain(self, domain):
        self.lock.acquire()
        self.already_occupied_fd.write(domain + '\n')
        self.already_occupied_fd.flush()
        self.lock.release()
        pass

    def add_uncheck_domain(self, domain):
        self.lock.acquire()
        self.uncheck_domain_list.append(domain)
        self.lock.release()
        pass

    def get_domain(self):
        if os.path.exists(self.set_uncheck_domain_file):
            words_file = gUncheckDomainFile
            with open(words_file, 'r') as fd:
                while True:
                    line = fd.readline()
                    if not line:
                        break
                    self.uncheck_domain_list.append(line[:-1])
        else:
            words_file = '/usr/share/dict/words'
            with open(words_file, 'r') as fd:
                while True:
                    line = fd.readline()
                    if not line:
                        break
                    self.uncheck_domain_list.append(line[:-1] + '.cc')
        print 'Load from [%s] Done, cnt [%d]' % (words_file, len(self.uncheck_domain_list))
        pass

    def get_domain_to_check(self):
        self.lock.acquire()
        if not len(self.uncheck_domain_list):
            ret_domain = None
        else:
            ret_domain = self.uncheck_domain_list.pop()
        self.lock.release()
        return ret_domain
        pass

    def save_uncheck_doman_list(self):
        with open(self.set_uncheck_domain_file, 'w+') as fd:
            for domain in self.uncheck_domain_list:
                fd.write(domain + '\n')
        pass

    def check_domain(self, domain_url):
        command = ['nslookup', domain_url]
        pipe = subprocess.Popen(command, stdout=subprocess.PIPE)
        out = ''
        while True:
            if pipe.poll() is not None:
                break
            time.sleep(0.1)
        out = pipe.stdout.read()
        ret = True
        pattern = 'server can\'t find'
        m = re.search(pattern, out)
        if m:
            print 'Not occupied [%s]' % domain_url
            ret = True

        pattern = 'answer'
        m = re.search(pattern, out)
        if m:
            print 'Already occupied [%s]' % domain_url
            ret = False
        return ret
        pass

    def check_domain_thread(self):
        self.running_thread_cnt += 1
        while True:
            domain = self.get_domain_to_check()
            if not domain:
                break
            ret = self.check_domain(domain)
            if ret:
                self.add_not_occupied_domain(domain)
            else:
                self.add_already_occupied_domain(domain)
            if self.quit:
                self.add_uncheck_domain(domain)
                break
        self.running_thread_cnt -= 1

    def start_scan(self):
        for idx in range(self.set_thread_cnt):
            pro = threading.Thread(target=self.check_domain_thread)
            pro.start()
        while True:
            try:
                time.sleep(5)
                if not len(self.uncheck_domain_list):
                    print 'All Done'
                    self.save_uncheck_doman_list()
                    return
            except KeyboardInterrupt:
                self.quit = True
                while 0 != self.running_thread_cnt:
                    print 'Please waiting for thread quit [%d]' % self.running_thread_cnt
                    time.sleep(1)
                self.save_uncheck_doman_list()
                print 'Quit Now'
                return
        pass

    def quit(self):
        pass


def do_test():
    scan_handle = ScanDomain()
    scan_handle.start_scan()
    pass

if __name__ == '__main__':
    do_test()