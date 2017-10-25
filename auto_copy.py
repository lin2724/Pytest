import os
import sys
import time

from common_lib import LogHandle

gLogHandle = LogHandle('copy.log')


def do_copy(from_dir, to_dir):
    items = os.listdir(from_dir)
    file_list = list()
    for item in items:
        path = os.path.join(from_dir, item)
        if os.path.isfile(path):
            file_list.append(path)
    gLogHandle.log ('Total file cnt [%d]' % len(file_list))
    if 0 == len(file_list):
        gLogHandle.log('All done')
        return True
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        dst_path = os.path.join(to_dir, file_name)
        gLogHandle.log('From [%s] to [%s]' % (file_path, dst_path))
        start_time = time.time()
        try:
            os.rename(file_path, dst_path)
        except KeyboardInterrupt:
            gLogHandle.log('Keyboard Except, quit now')
            exit(0)
        except:
            e = sys.exc_info()[0]
            gLogHandle.log('Failed move %s' % e)
            gLogHandle.log('Failed Time use [%d]s' % (time.time() - start_time))

        gLogHandle.log('Time use [%d]s' % (time.time() - start_time))
    return False
    pass

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage python %s <from_dir> <to_dir>' % __file__
        exit(0)
    while True:
        ret = do_copy(sys.argv[1], sys.argv[2])
        if ret:
            gLogHandle.log('Quit Now')
            exit(0)