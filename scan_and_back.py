import os
import time
import sys
from common_lib import MyArgParse
from common_lib import ConColorShow
from common_lib import ConColor

G_default_filter_tail = list()

G_build_folder_path = '/home/w01208/z03467/sp90_others/build/'
G_store_folder_path = '/home/w01208/z03467/All_libs/sp90_120'

gBuildIPC = True

G_build_folder_bin_path = os.path.join(G_build_folder_path, 'bin/x86_64/debug/')
G_build_folder_lib_path = os.path.join(G_build_folder_path, 'dll/x86_64/debug/')
G_store_folder_bin_path = os.path.join(G_store_folder_path, 'bin')
G_store_folder_lib_path = os.path.join(G_store_folder_path, 'lib')

if gBuildIPC:
    G_build_folder_lib_path = os.path.join(G_build_folder_path, 'dll/arm_ipc/debug')

class Bcolors:

    def __init__(self):
        pass
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    if os.name == 'nt':
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''


def color_test():
    print Bcolors.HEADER + 'HEADER' + Bcolors.ENDC
    print Bcolors.OKBLUE + 'OKBLUE' + Bcolors.ENDC
    print Bcolors.OKGREEN + 'OKGREEN' + Bcolors.ENDC
    print Bcolors.WARNING + 'WARNING' + Bcolors.ENDC
    print Bcolors.FAIL + 'FAIL' + Bcolors.ENDC


def filter_tail(file_name, filter_tails):
    if not len(filter_tails):
        return True
    for filter_tail in filter_tails:
        if file_name[-len(filter_tail):] == filter_tail:
            return False
    return True
    pass


def scan_new_files(scan_folder, time_gap):
    global G_default_filter_tail
    try:
        time_min = int(time_gap)
    except ValueError:
        print 'ERROR:only number!'
        return None
    limit_sec = time_min*60
    now_sec = time.time()
    new_file_full_path_list = list()
    scan_folder_list = list()
    if type(scan_folder) == list:
        scan_folder_list = scan_folder
    else:
        scan_folder_list.append(scan_folder)
    for scan_folder in scan_folder_list:
        if not os.path.exists(scan_folder):
            print 'folder [%s] not exist!' % scan_folder
            return None
        file_list = os.listdir(scan_folder)
        changed_file_cnt = 0
        for file_name in file_list:
            full_file_path = os.path.join(scan_folder, file_name)
            if os.path.isfile(full_file_path):
                stat = os.stat(full_file_path)
                if stat.st_mtime + limit_sec >= now_sec:
                    if filter_tail(full_file_path, G_default_filter_tail):
                        print Bcolors.HEADER + '%24s  %12s' % (file_name, time.ctime(stat.st_mtime)) + Bcolors.ENDC
                        new_file_full_path_list.append(full_file_path)
                        changed_file_cnt += 1
        print '### Dir %s Total[%d] changed [%d]###' % (scan_folder, len(file_list), changed_file_cnt)
    return new_file_full_path_list
    pass


def scan_new_files_recursive(scan_folders, time_gap):
    global G_default_filter_tail
    try:
        time_min = int(time_gap)
    except ValueError:
        print 'ERROR:only number!'
        return None
    limit_sec = time_min*60
    now_sec = time.time()
    new_file_full_path_list = list()
    scan_folder_list = list()
    if type(scan_folders) == list:
        scan_folder_list = scan_folders
    else:
        scan_folder_list.append(scan_folders)
    for scan_folder in scan_folder_list:
        if not os.path.exists(scan_folder):
            print 'folder [%s] not exist!' % scan_folder
            return None
        changed_file_cnt = 0
        file_count_folder = 0
        for (dirpath, dirnames, filenames) in os.walk(scan_folder):
            for filename in filenames:
                file_count_folder += 1
                full_file_path = os.path.join(dirpath, filename)
                stat = os.stat(full_file_path)
                if stat.st_mtime + limit_sec >= now_sec:
                    if filter_tail(full_file_path, G_default_filter_tail):
                        print Bcolors.HEADER + '%24s  %12s' % (filename, time.ctime(stat.st_mtime)) + Bcolors.ENDC
                        new_file_full_path_list.append(full_file_path)
                        changed_file_cnt += 1
            print '### Dir %s Total[%d] changed [%d]###' % (scan_folder, file_count_folder, changed_file_cnt)
    return new_file_full_path_list


def files_copy_to_folder(full_path_file_list, folder_des):
    if not os.path.exists(folder_des):
        os.system('mkdir -p %s' % folder_des)
        print '%s not exist create it' % folder_des
    for full_file_path in full_path_file_list:
        if not os.path.exists(full_file_path):
            print 'ERROR:file %s not exist!' % full_file_path
            return
        os.system('/bin/cp -fv %s %s' % (full_file_path, folder_des))
    pass


def scan_and_copy_changed_bin_lib(time_gap, copy_cmd):
    full_changed_lib_files_path = scan_new_files(G_build_folder_lib_path, time_gap)
    if not gBuildIPC:
        full_changed_bin_files_path = scan_new_files(G_build_folder_bin_path, time_gap)
    if copy_cmd:
        files_copy_to_folder(full_changed_lib_files_path, G_store_folder_lib_path)
        if not gBuildIPC:
            files_copy_to_folder(full_changed_bin_files_path, G_store_folder_bin_path)
    pass


def clear_folder(folder_to_clean):
    global G_store_folder_path
    full_path_folder = folder_to_clean
    ConColorShow().warning_show('do clean at %s' % full_path_folder)
    if full_path_folder in ['/', '/home', '/root']:
        ConColorShow().error_show('!!!are you mad to delete %s' % folder_to_clean)
        exit(1)
    s = raw_input(ConColor.Red + '---> input y to continue [y/n]' + ConColor.Reset)
    if s.lower() == 'y':
        os.system('rm -rvf %s' % full_path_folder)
    else:
        print 'nothing done'
    pass


def arg_parser_init():
    arg_parse = MyArgParse()
    arg_parse.add_option('-cp', [0, 1], '-cp [desc_folder]: do copy from scan list')
    arg_parse.add_option('-d', 1, 'specific dir to scan')
    arg_parse.add_option('-t', 1, '-t <sec_time>: min time specific')
    arg_parse.add_option('-clear', [0, 1], '-clear [folder]: clear folder')
    arg_parse.add_option('-p', 0, 'print default scan folder and des folder')
    arg_parse.add_option('-r', 0, 'recursive scan folder')
    arg_parse.add_option('-h', 0, 'print help')
    return arg_parse
    pass


if __name__ == '__main__':
    G_default_filter_tail.append('.a')

    arg_parser = arg_parser_init()
    if not arg_parser.parse(sys.argv):
        ConColorShow().error_show('please input valid args')
        print arg_parser
        exit(1)
        pass

    if arg_parser.check_option('-p'):
        ConColorShow().highlight_show('scan folder base %s' % G_build_folder_path)
        ConColorShow().highlight_show('store folder base %s'% G_store_folder_path)
        exit(0)

    if arg_parser.check_option('-clear'):
        folder_args = arg_parser.get_option_args('-clear')
        if len(folder_args):
            clear_folder(folder_args[0])
        else:
            clear_folder(G_store_folder_path)
        exit(0)

    if not arg_parser.check_option('-t'):
        ConColorShow().warning_show('<-t time> arg is needed!')
        print arg_parser
        exit(1)
    time_gap = int(arg_parser.get_option_args('-t')[0])

    if arg_parser.check_option('-d'):
        scan_folder = arg_parser.get_option_args('-d')[0]
        if arg_parser.check_option('-r'):
            new_files = scan_new_files_recursive(scan_folder, time_gap)
        else:
            new_files = scan_new_files(scan_folder, time_gap)
        if arg_parser.check_option('-cp'):
            store_folder_args = arg_parser.get_option_args('-cp')
            if len(store_folder_args):
                desc_store_folder = store_folder_args[0]
                files_copy_to_folder(new_files, desc_store_folder)
            else:
                ConColorShow().error_show('<-desc folder> is needed if you specific scan_folder by hand')
                exit(1)
        exit(0)

    if arg_parser.check_option('-cp'):
        store_folder_args = arg_parser.get_option_args('-cp')
        if len(store_folder_args):
            desc_store_folder = store_folder_args[0]
            full_changed_lib_files_path = scan_new_files(G_build_folder_lib_path, time_gap)
            if not gBuildIPC:
                full_changed_bin_files_path = scan_new_files(G_build_folder_bin_path, time_gap)
            files_copy_to_folder(full_changed_lib_files_path, desc_store_folder)
            if not gBuildIPC:
                files_copy_to_folder(full_changed_bin_files_path, desc_store_folder)
        else:
            scan_and_copy_changed_bin_lib(time_gap, True)
    else:
        scan_and_copy_changed_bin_lib(time_gap, False)

    exit(0)

