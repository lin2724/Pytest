import os
import sys
import re
from common_lib import MyArgParse

def get_file_tail(file_name):
    ret_list = file_name.split('.')
    if len(ret_list) > 1:
        return ret_list[len(ret_list)-1]
    return ''
    pass


def search(search_folder, filename, file_tail):
    print 'Search for %s , tail [%s]' % (filename, file_tail)
    ret_file_list = list()
    ret_folder_list = list()
    if not os.path.exists(search_folder):
        print 'Folder [%s] not exist!'
        return ret_folder_list, ret_file_list
    for root, folders, files in os.walk(search_folder):
        for file_name in files:
            tail = get_file_tail(file_name)
            if tail == file_tail:
                if filename not in file_name:
                    continue
                full_path = os.path.join(root, file_name)
                ret_file_list.append(full_path)
        if len(file_tail):
            for folder_name in folders:
                if filename in folder_name:
                    ret_folder_list.append(folder_name)
    print 'Folder cnt [%d], file cnt [%d]' % (len(ret_folder_list), len(ret_file_list))
    return ret_folder_list, ret_file_list


def search_content(file_list, pattern):
    for file_path in file_list:
        with open(file_path, 'r') as fd:
            while True:
                buf = fd.readline()
                if not buf:
                    break
                m = re.search(pattern, buf)
                if m:
                    print 'Got [%s]' % buf
    pass


def arg_parser_init():
    arg_parse = MyArgParse()
    arg_parse.add_option('-d', [1], 'folder to search')
    arg_parse.add_option('-name', [1], 'part file name to search ')
    arg_parse.add_option('-tail', [1], 'file tail [optional]')
    arg_parse.add_option('-p', [1], 'search content pattern [optional]')
    arg_parse.add_option('-h', [0], 'show help info')
    return arg_parse


def main():
    arg_parse = arg_parser_init()
    arg_parse.parse(sys.argv)
    if not arg_parse.check_option('-d') or not arg_parse.check_option('-name'):
        print arg_parse
        return
    tail = ''
    if arg_parse.check_option('-tail'):
        tail = arg_parse.get_option_args('-tail')[0]
    (folders, files) = search(arg_parse.get_option_args('-d')[0], arg_parse.get_option_args('-name')[0], tail)
    for folder in folders:
        print folder
    for file_name in files:
        print file_name

    if arg_parse.check_option('-p'):
        print 'search for pattern [%s]' % arg_parse.get_option_args('-p')[0]
        search_content(files, arg_parse.get_option_args('-p')[0])

if __name__ == '__main__':
    main()
