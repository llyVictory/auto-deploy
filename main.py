import sys
import traceback

from config import Config
from ssh_manager import SSHManager
from builder import build_jar_package
from process_manager import (
    find_and_kill_java_process_by_jps,
    backup_old_jar,
    start_and_tail_log,
)
from uploader import upload_jar
from utils import wait_for_exit


def main():
    try:
        # 加载配置
        config = Config()

        local_target_jar = config.get_local_target_jar()
        remote_jar_path = config.get_remote_jar_path()

        print("🚨 🚨 确认：1.微服务发版将bootstrap.yml调成服务器环境！2.inode开启！3.服务器vpn（若有）开启！")
        print("▶️后端发版开始！")

        # 1. 构建
        print("1.构建 JAR 包...")
        if not build_jar_package(config):
            return

        # 2. 连接 SSH
        print("2.连接远程服务器...")
        ssh_manager = SSHManager(
            config.remote_host,
            config.remote_port,
            config.remote_user,
            config.remote_pass,
        )
        if not ssh_manager.connect():
            return

        # 3. 杀死旧进程
        print("3.查找并终止旧的 Java 进程...")
        find_and_kill_java_process_by_jps(ssh_manager, config)

        # 4. 备份旧包
        print("4.备份旧的 JAR 包...")
        backup_old_jar(ssh_manager, config)

        # 5. 上传新包
        print("5.上传新的 JAR 包...")
        if not upload_jar(config, local_target_jar, remote_jar_path):
            return

        # 6. 启动并查看日志
        print("6.启动新程序并查看日志...")
        start_and_tail_log(ssh_manager, config)

    except Exception:
        print("❌ 程序异常，详细错误如下：")
        traceback.print_exc()
        print("\n程序异常，请检查日志，按右上角关闭终端。")
        wait_for_exit()
    finally:
        try:
            ssh_manager.close()
        except Exception:
            pass

        print("程序终止，等待终端关闭......")
        from utils import wait_for_exit
        wait_for_exit()  # 阻止自动关闭终端，直到你点击右上角 X


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ 捕获到 Ctrl+C，程序退出。")

