import paramiko
import sys

class SSHManager:
    def __init__(self, host, port, username, password):
        self.ssh = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )
            print(" 服务器连接成功!")
            return True
        except Exception as e:
            print(" SSH 连接失败，详细错误如下：")
            print(str(e))
            print(" 请检查远程连接配置或网络状况，按右上角关闭终端。")
            return False

    def exec_command(self, command, timeout=None):
        if not self.ssh:
            raise RuntimeError("SSH未连接")
        return self.ssh.exec_command(command, timeout=timeout)

    def close(self):
        if self.ssh:
            try:
                self.ssh.close()
                print("️ SSH 连接已关闭")
            except Exception as e:
                print(f" 关闭SSH连接异常: {e}")
            self.ssh = None