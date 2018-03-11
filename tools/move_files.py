import os
import sys


class MoveOperation:
    def __init__(self):
        self.m_destination_folder = 'default_destination'
        self.m_scan_folder_path = ''

        self.m_list_to_move_files = list()
        self.m_list_failed_move_files = list()

        self.m_set_dummy = False
        self.m_set_action_mode = 'list'

        self.m_func_check = self.template_check_if_move

        self.do_init()
        pass

    def do_init(self):
        pass

    def log(self, log_str):
        print (log_str)
        pass

    def load_check_functionj(self, check_func):
        self.m_func_check = check_func
        pass

    def set_action(self, action_str):
        self.m_set_action_mode = action_str.lower()

    def set_destination(self, folder_path):
        self.m_destination_folder = folder_path
        pass

    def set_check_folder(self, folder_path):
        self.m_scan_folder_path = folder_path
        pass

    def check_if_move(self, folder_path, file_name):
        return self.m_func_check(folder_path, file_name)
        pass

    def template_check_if_move(self, folder_path, file_name):
        # self.log('check [%s]' % file_name)
        if file_name.lower().endswith('.jpg') or file_name.lower().endswith('.jpeg'):
            return True
        return False
        pass

    def do_scan(self):
        if not os.path.exists(self.m_scan_folder_path):
            self.log('Folder not exist [%s]' % self.m_scan_folder_path)
            return
        for root, folders, files in os.walk(self.m_scan_folder_path):
            for file_name in files:
                file_full_path = os.path.join(root, file_name)
                if self.check_if_move(root, file_name):
                    self.m_list_to_move_files.append(file_full_path)
            pass
        pass

    def do_action(self):
        if not os.path.exists(self.m_destination_folder):
            os.makedirs(self.m_destination_folder)
        mode = 0
        if self.m_set_action_mode == 'list':
            mode = 0
        elif self.m_set_action_mode == 'copy':
            mode = 1
        elif self.m_set_action_mode == 'move':
            mode = 2
        while True:
            if not len(self.m_list_to_move_files):
                break
            file_path = self.m_list_to_move_files.pop()
            file_name = os.path.basename(file_path)
            des_path = os.path.join(self.m_destination_folder, file_name)
            try:
                if 0 == mode:
                    self.log('[%s]' % file_path)
                    pass
                elif 1 == mode:
                    if os.path.exists(des_path):
                        self.log('Dest path already exist [%s]' % des_path)
                        self.m_list_failed_move_files.append(file_path)
                        continue
                    with open(des_path, 'wb+') as fd:
                        with open(file_path, 'rb') as fd_r:
                            fd.write(fd_r.read())
                    self.log('copy [%s] to [%s]' % (file_path, des_path))
                elif 2 == mode:
                    if os.path.exists(des_path):
                        self.log('Dest path already exist [%s]' % des_path)
                        self.m_list_failed_move_files.append(file_path)
                        self.log('move [%s] to [%s]' % (file_path, des_path))
                        continue
                    os.rename(dst=des_path, src=file_path)
                # self.log('[%s] to [%s]' % (file_path, des_path))
            except OSError:
                self.log('Failed to move from [%s] to [%s]' % (file_path, des_path))
                self.m_list_failed_move_files.append(file_path)
        pass

    def go(self, action='list'):
        self.set_action(action)
        self.do_scan()
        self.do_action()
        self.log('Done')
        pass


def check_gif(root, file_name):
    if file_name.lower().endswith('gif'):
        return True
    return False


def test(check_folder, des_folder, action='list'):
    scan_hanlder = MoveOperation()
    scan_hanlder.set_check_folder(check_folder)
    scan_hanlder.set_destination(des_folder)
    scan_hanlder.load_check_functionj(check_gif)
    scan_hanlder.go(action)
    pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: python %s scan_folder store_folder' % __file__
        exit(0)
        pass
    if len(sys.argv) == 4:
        test(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        test(sys.argv[1], sys.argv[2])

