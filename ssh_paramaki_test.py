import paramiko
import socket
import time
import os


class SSHClient:
    def __init__(self):
        self.server_ip = ''
        self.username = ''
        self.passwd = ''
        self.port = 22
        self.ssh = paramiko.SSHClient()
        self.sftp = None
        self.is_init = False
        pass

    def connect(self, server_ip, username, password, port=22):
        self.server_ip = server_ip
        self.username = username
        self.passwd = password
        self.port = port

        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try_time = 10
        while try_time:
            try:
                self.ssh.connect(self.server_ip, self.port, self.username, self.passwd)
                # self.sftp = paramiko.SFTPClient.from_transport(self.ssh.get_transport())
                self.sftp = self.ssh.open_sftp()
                self.is_init = True
                break
            except socket.error:
                print 'ERROR:connect to %s fail' % self.server_ip
            except paramiko.ssh_exception.AuthenticationException:
                print 'ERROR:passwd or username wrong!'
                pass
            try_time -= 1
            time.sleep(0.1)
        return self.is_init
        pass

    def upload_file(self, local_path, server_path):
        self.sftp.put(local_path, server_path)
        pass

    def download_file(self, server_path, local_path):
        self.sftp.get(server_path, local_path)
        pass

    def send_command(self):
        pass

