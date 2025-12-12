import time
import sys

def find_and_kill_java_process_by_jps(ssh_manager, config):
    print(f" 使用 jps 查找 {config.local_jar_name} 主进程...")
    jps_cmd = f"{config.jps_exec} -l | grep {config.local_jar_name}"
    stdin, stdout, stderr = ssh_manager.exec_command(jps_cmd)
    output = stdout.read().decode().strip()

    if not output:
        print(f"️ jps 未找到匹配的 {config.local_jar_name} 主进程。")
        return

    lines = output.splitlines()
    pids = []
    for line in lines:
        print(f" jps 输出行：{line}")
        parts = line.strip().split()
        if len(parts) >= 2 and parts[1].endswith(config.local_jar_name):
            pid = parts[0]
            pids.append(pid)

    if not pids:
        print("️ 未提取到合法 PID")
        return

    print(f" 共找到 {len(pids)} 个 {config.local_jar_name} 主进程：{', '.join(pids)}")

    for pid in pids:
        print(f" 正在 kill PID={pid} ...")
        ssh_manager.exec_command(f"kill -9 {pid}")
        time.sleep(3)

        check_cmd = f"ps -p {pid}"
        stdin_check, stdout_check, _ = ssh_manager.exec_command(check_cmd)
        check_output = stdout_check.read().decode().strip()

        if pid in check_output:
            print(f" 进程 PID={pid} 杀不掉！")
            print(f" 查看 /proc/{pid}/status ...")
            stdin_ps, stdout_ps, _ = ssh_manager.exec_command(f"cat /proc/{pid}/status")
            print(" 状态输出：\n" + stdout_ps.read().decode().strip())

            print(f" {config.local_jar_name} 主进程无法杀死，本程序终止，请手动检查服务器")
            ssh_manager.close()
            sys.exit(1)
        else:
            print(f" PID={pid} 杀死成功")

    print(f" 所有涉及 {config.local_jar_name} 主进程已终止")

def backup_old_jar(ssh_manager, config):
    import datetime
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        cmd_backup = (
            f"cd {config.remote_path} && mv {config.local_jar_name} {config.local_jar_name}.{timestamp}"
        )
        ssh_manager.exec_command(cmd_backup)
        print(" 备份旧包完成：", f"{config.local_jar_name}.{timestamp}")
    except Exception as e:
        print(" 备份旧包失败：")
        print(e)
        print("请检查远程目录权限或文件是否存在")
        # 建议这里不要直接退出，主流程判断

def start_and_tail_log(ssh_manager, config):
    import time

    # 启动远程程序
    ssh_manager.exec_command(
        f"cd {config.remote_path} && nohup {config.java_exec} -jar {config.local_jar_name} > {config.remote_log_file} 2>&1 &"
    )
    time.sleep(2)

    # 实时打印日志
    print("▶️ 实时查看日志中...（关闭窗口可中止）")
    try:
        stdin, stdout, stderr = ssh_manager.exec_command(
            f"cd {config.remote_path} && tail -F {config.remote_log_file}"
        )

        for line in iter(lambda: stdout.readline(2048), ""):
            if line:
                print(line.strip())
            else:
                break  # 文件尾部无内容，终止读取

    except Exception as e:
        print("❌ 日志查看过程中发生错误：")
        print(e)
        print("可能原因：远程路径错误 / 权限不足 / 程序未正常启动")
        return False

    return True
