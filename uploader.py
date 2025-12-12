import paramiko
import os
import sys

def upload_jar(config, local_target_jar, remote_jar_path):
    print("️正在上传新包...")

    def print_progress(transferred, total):
        percent = transferred / total * 100
        bar = '=' * int(40 * percent / 100) + '-' * (40 - int(40 * percent / 100))
        sys.stdout.write(f"\r[{bar}] {percent:.2f}%")
        sys.stdout.flush()

    try:
        transport = paramiko.Transport((config.remote_host, config.remote_port))
        transport.connect(username=config.remote_user, password=config.remote_pass)
        sftp = paramiko.SFTPClient.from_transport(transport)

        file_size = os.path.getsize(local_target_jar)
        transferred = 0

        with open(local_target_jar, 'rb') as f_local, sftp.file(remote_jar_path, 'wb') as f_remote:
            while True:
                data = f_local.read(32768)
                if not data:
                    break
                f_remote.write(data)
                transferred += len(data)
                print_progress(transferred, file_size)

        f_remote.flush()
        f_remote.close()
        sftp.close()
        transport.close()

        print("\n 上传完成")
        return True

    except Exception as e:
        print(" 上传过程中发生异常：")
        print(e)
        print(" 请检查网络、权限或远程路径设置，按右上角关闭终端。")
        return False