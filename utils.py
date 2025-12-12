# utils.py
import time

def wait_for_exit():
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n⚠️ 捕获到 Ctrl+C，程序继续等待终端关闭。")
