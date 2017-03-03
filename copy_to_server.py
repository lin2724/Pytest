import paramiko
import socket
import os
import time
import sys
import ConfigParser
from common_lib import CfgParse
from common_lib import ConColor
from common_lib import ConColorShow
from common_lib import MyArgParse

G_config_file = 'copy_to_server.cfg'

G_scan_filter_tail = list()


def filter_tail(file_name, filter_tails):
    if not len(filter_tails):
        return True
    for filter_tail in filter_tails:
        if file_name[-len(filter_tail):] == filter_tail:
            return False
    return True
    pass


def scan_new_files(scan_folder, time_gap):
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
                    if filter_tail(full_file_path, G_scan_filter_tail):
                        ConColorShow().color_show('%24s  %12s' % (file_name, time.ctime(stat.st_mtime)) , ConColorShow.Green)
                        new_file_full_path_list.append(full_file_path)
                        changed_file_cnt += 1
        print '### Dir %s Total[%d] changed [%d]###' % (scan_folder, len(file_list), changed_file_cnt)
    return new_file_full_path_list
    pass


def scan_new_files_v2(scan_folder, time_gap):
    """
    time_gap:>0 scan file changed within time_gap(sec) from now
             =0 will scan and return all files in scan_folder
    """
    try:
        time_min = int(time_gap)
    except ValueError:
        print 'ERROR:only number! %s' % time_gap
        return None
    limit_sec = time_min*60
    now_sec = time.time()
    new_file_full_path_list = list()
    scan_folder_list = list()
    start_time = time.time()
    if type(scan_folder) == list:
        scan_folder_list = scan_folder
    else:
        scan_folder_list.append(scan_folder)
    for scan_folder in scan_folder_list:
        if not os.path.exists(scan_folder):
            print 'folder [%s] not exist!' % scan_folder
            return None
        for (dirpath, dirnames, filenames) in os.walk(scan_folder):
            #stat = os.stat(dirpath)
            #if stat.st_mtime + limit_sec < now_sec:
            #    continue
            for filename in filenames:
                stat = os.stat(os.path.join(dirpath, filename))
                if stat.st_mtime + limit_sec >= now_sec or limit_sec == 0:
                    new_file_full_path = os.path.join(dirpath, filename)
                    ConColorShow().color_show('%24s  %12s' % (filename, time.ctime(stat.st_mtime)), ConColorShow.Green)
                    new_file_full_path_list.append(new_file_full_path)
            pass
    print '### Dir %s changed count [%d]###' % (scan_folder, len(new_file_full_path_list))
    print 'time use %f' % (time.time() - start_time)
    return new_file_full_path_list
    pass


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


class SSHHandle:
    def __init__(self, server_ip, username, password):
        self.server_ip = server_ip
        self.username = username
        self.passwd = password
        self.port = 22
        self.ssh = paramiko.SSHClient()
        self.sftp = None
        self.do_init()
        pass

    def do_init(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(self.server_ip, self.port, self.username, self.passwd)
            self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
            self.sftp = self.ssh.open_sftp()
        except socket.error:
            print 'ERROR:connect to %s fail' % self.server_ip
        except paramiko.ssh_exception.AuthenticationException:
            print 'ERROR:passwd or username wrong!'
            pass

    def copy_file_from_server(self, server_path, local_path):
        self.sftp.get(server_path, local_path)
        pass

    def check_folder_exist(self, folder_path):
        pass

    def copy_file_to_server(self, server_path, local_path):
        self.sftp.put(local_path, server_path)
        pass
    pass


def copy_local_to_server(local_files):
    global G_server_ip
    global G_username
    global G_password
    global G_server_base_path
    global G_local_base_path
    ssh_handle = SSHHandle(server_ip=G_server_ip, username=G_username, password=G_password)
    for local_file_full_path in local_files:
        remote_path_tail = get_tail_path(G_local_base_path, local_file_full_path)
        remote_file_full_path = os.path.join(G_server_base_path, remote_path_tail).replace('\\', '/')
        try:
            ssh_handle.copy_file_to_server(remote_file_full_path, local_file_full_path)
        except IOError:
            e = sys.exc_info()[0]
            print e
            ConColorShow().error_show('Fail to copy from %s to %s' % (remote_file_full_path, local_file_full_path))
            s = raw_input("--continue?[y/n]").lower()
            if s == 'y':
                continue
            ConColorShow().error_show('stop')
            exit(1)
        print 'copy to server done %s ' % local_file_full_path
    pass


def get_tail_path(base_path, full_path):
    if len(full_path) <= len(base_path):
        print 'ERROR:wrong file path! %s'
        return None
    for i in range(min(len(base_path), len(full_path))):
        if base_path[i].lower() != full_path[i].lower():
            return full_path[i:]
    tail_path =  full_path[min(len(base_path), len(full_path)):]
    if tail_path[:1] == '/' or tail_path[:1] == '\\':
        tail_path = tail_path[1:]
    return tail_path
    pass

G_server_ip = ''
G_username = ''
G_password = ''
G_server_base_path = ''
G_local_base_path = ''


def default_config_init():
    global G_config_file
    parser = CfgParse(G_config_file)
    if parser.check_cfg_empty():
        parser.fill_default_cfg('[Config]\n'
                                'server_ip=207.207.69.177\n'
                                'username=root\n'
                                'password = 123456\n'
                                'G_server_base_path = /home/z03467/h1226/h1226\n'
                                'G_local_base_path=E:\StoreceCode_main\D115SP90_120\n'
                                'scan_dir_list_max=10\n'
                                'scan_dir_1=IMOS_CODE_CDS\imos\server\src\n'
                                'scan_dir_2=IMOS_CODE_BP\imos\server\include'
                                )
    global G_server_ip
    global G_username
    global G_password
    global G_server_base_path
    global G_local_base_path
    G_server_ip = parser.get('Config', 'server_ip')
    G_username = parser.get('Config', 'username')
    G_password = parser.get('Config', 'password')
    G_server_base_path = parser.get('Config', 'G_server_base_path')
    G_local_base_path = parser.get('Config', 'G_local_base_path')

    return parser
    pass


def get_scan_dir_list():
    parser = default_config_init()
    scan_dir_list_max = parser.get('Config', 'scan_dir_list_max')
    scan_dir_list = list()
    for i in range(1, int(scan_dir_list_max) + 1):
        try:
            scan_dir = parser.get('Config', 'scan_dir_%d' % i)
            scan_dir = os.path.join(G_local_base_path, scan_dir)
            scan_dir_list.append(scan_dir)
        except ConfigParser.NoOptionError:
            break
    return scan_dir_list
    pass


def arg_parser_init():
    arg_parse = MyArgParse()
    arg_parse.add_option('-t', [1], 'time(sec) specific, to detect file change')
    arg_parse.add_option('-cp', [0], 'do copy')
    arg_parse.add_option('-update', [0], 'copy new files from remote')
    arg_parse.add_option('-h', [0], 'show help info')
    return arg_parse

if __name__ == '__main__':
    parser = default_config_init()
    arg_parser = arg_parser_init()
    scan_dir_list = get_scan_dir_list()
    G_scan_filter_tail.append('.a')
    if not arg_parser.parse(sys.argv):
        ConColorShow().error_show('please input valid args')
        print arg_parser
        exit(1)
        pass

    if arg_parser.check_option('-update'):
        new_file_list = scan_new_files_v2(scan_dir_list, 0)
        copy_local_to_server(new_file_list)
        exit(0)

    time_gap = None
    if arg_parser.check_option('-t'):
        time_gap = arg_parser.get_option_args('-t')[0]
    else:
        ConColorShow().error_show('please specific time')
        exit(1)

    new_file_list = scan_new_files_v2(scan_dir_list, time_gap)
    if arg_parser.check_option('-cp'):
        copy_local_to_server(new_file_list)



























