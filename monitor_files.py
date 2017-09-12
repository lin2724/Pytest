import os
import sys
import time
import datetime
import threading
from common_lib import LogHandle


class MonitorFile:
    def __init__(self):
        self.set_monitor_period_sec = 3
        self.set_log_file_path = 'monitor_files.log'
        self.logHandle = LogHandle(self.set_log_file_path)
        self.set_store_path = ''

        self.lock = threading.Lock()
        self.monitor_file_list = list()
        self.change_file_list = list()

        self.alive_thread_cnt = 0
        self.need_quit = False

        pass

    def add_monitor_file(self, file_path):
        dict_item = dict()
        dict_item['file_path'] = file_path[:]
        dict_item['last_change_time'] = None
        self.lock.acquire()
        self.monitor_file_list.append(dict_item)
        self.lock.release()
        pass

    def delete_monitor_file(self, file_path):
        pass

    def set_monitor_period(self, time_sec):
        pass

    def set_store_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        self.set_store_path = folder_path[:]

    def get_new_file_path(self, old_file_path):
        file_name = os.path.basename(old_file_path)
        cur_datetime = datetime.datetime.now()
        new_file_path = os.path.join(self.set_store_path, file_name)
        for c in str(cur_datetime):
            if '0' <= c <= '9':
                new_file_path += c
        return new_file_path
        pass

    def do_if_change(self, file_path):
        max_size_once_read = 1*1024*1024
        new_file_name = self.get_new_file_path(file_path)
        if os.path.exists(new_file_name):
            self.logHandle.log('Warning, back file already exist [%s]' % new_file_name)
            return
        with open(new_file_name, 'w+') as w_fd:
            with open(file_path, 'r') as r_fd:
                while True:
                    content = r_fd.read(max_size_once_read)
                    if not content:
                        break
                    w_fd.write(content)
        self.logHandle.log('Copy [%s] to [%s]' % (file_path, new_file_name))
        pass

    def start(self):
        pro = threading.Thread(target=self.monitor_thread)
        pro.start()
        pass

    def stop(self):
        self.need_quit = True
        while self.alive_thread_cnt:
            self.logHandle.log('waiting for thread quit...')
            time.sleep(0.5)
        self.logHandle.log('Quit now')

    def monitor_thread(self):
        self.alive_thread_cnt += 1
        while True:
            self.lock.acquire()
            for file_item in self.monitor_file_list:
                file_path = file_item['file_path']
                time_info = file_item['last_change_time']
                self.logHandle.log('Check files [%s]' % file_path)
                if os.path.exists(file_path):
                    file_stat = os.stat(file_path)
                    if file_stat.st_mtime != time_info:
                        self.change_file_list.append(file_item)
                        cur_time_info = file_stat.st_mtime
                        file_item['last_change_time'] = cur_time_info
                        self.logHandle.log('Add File [%s] to change list' % file_path)
            for file_item in self.change_file_list:
                self.logHandle.log('File [%s] will be processed' % file_item['file_path'])
                self.do_if_change(file_item['file_path'])
            self.change_file_list = list()
            self.lock.release()
            if self.need_quit:
                break
            time.sleep(self.set_monitor_period_sec)
            if self.need_quit:
                break
        self.alive_thread_cnt -= 1
        pass

def test():
    monitor_handle = MonitorFile()
    monitor_handle.add_monitor_file('/var/log/imoslog/cds_ndserver01.log')
    monitor_handle.add_monitor_file('/var/log/imoslog/cds_ndserver01.debug')
    monitor_handle.set_store_folder('./logback')
    monitor_handle.start()
    while True:
        try:
            time.sleep(10)
        except KeyboardInterrupt:
            monitor_handle.stop()
            exit(0)
    pass

if __name__ == '__main__':
    test()

