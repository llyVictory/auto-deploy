import os
import subprocess
import sys
from utils import wait_for_exit  # 需要你创建一个utils.py，放公共函数
def build_jar_package(config):
    try:
        print(f"️ 开始构建 {config.local_jar_name} 包...")
        os.chdir(config.local_project_dir)

        build_cmd = (
            f'"{config.mvn_cmd}" clean install -DskipTests '
            f'-s "{config.maven_settings}" '
            f'-Dmaven.repo.local={config.maven_repo}'
        )
        print(f"️ 执行命令：{build_cmd}")

        # 🔧🔧🔧【关键补充】让 Maven 使用你 .env 里的 JDK21
        env = os.environ.copy()
        if config.local_java_home:  # <-- 你自己读取的 LOCAL_JAVA_HOME
            env["JAVA_HOME"] = config.local_java_home
            env["PATH"] = config.local_java_home + r"\bin;" + env["PATH"]

        process = subprocess.Popen(
            build_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            env=env   # 🔥🔥🔥 关键：把 JDK21 环境变量传给子进程
        )

        for line in process.stdout:
            print(line.rstrip())

        retcode = process.wait()
        if retcode != 0:
            print(f" {config.local_jar_name}构建失败，返回码：", retcode)
            print(f" {config.local_jar_name}构建失败，请检查日志，按右上角关闭终端。")
            wait_for_exit()
            return False
        else:
            print(f" {config.local_jar_name} 构建成功!")
            return True

    except Exception as e:
        print(f" {config.local_jar_name}构建过程中出现异常：", str(e))
        wait_for_exit()
        return False
