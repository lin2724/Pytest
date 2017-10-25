import os
import sys

from common_lib import LogHandle


def do_copy(from_dir, to_dir):
    items = os.listdir(from_dir)
    file_list = list()
    for item in items:
        path = os.path.join(from_dir, item)
        if os.path.isfile(path):
            file_list.append(path)
    print 'Total file cnt [%d]' % len(file_list)
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        dst_path = os.path.join(to_dir, file_name)
        print 'From [%s] to [%s]' % (file_path, dst_path)
    pass

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage python %s <from_dir> <to_dir>' % __file__
        exit(0)
    do_copy(sys.argv[1], sys.argv[2])