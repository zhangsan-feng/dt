import os
import re
import time
import random
import uuid
from pynvml import *
import psutil
import pyautogui

def match_url(text):
    if not text:
        return None
    regex = r'https?://[^\s]+'
    match = re.search(regex, text)
    if match:
        return match.group(0)
    else:
        return None


def word_analysis(text):
    text = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '', text)
    if len(text) > 30:
        return text[:30]
    return text

def max_index(obj, key):
    m = 0
    index = 0
    for i in range(len(obj)):
        if obj[i][key] > m:
            m = obj[i][key]
            index = i
    return index


def gen_uid():
    timestamp = int(time.time() * 1000000)
    random_number = random.randint(10 ** (15 - 1), 10 ** 15 - 1)
    random_str = f"{random_number:015d}"
    result = f"{timestamp}{random_str}"
    return result

def random_sleep():
    time.sleep(random.uniform(3.0, 6.0))


def get_cookie_key(cookie, k):
    cookie_list = cookie.split(";")
    for ck in cookie_list:
        ck_list = ck.split("=")
        if len(ck_list) != 2:
            continue
        key, value = ck_list[0], ck_list[1]
        # print(key, value)
        if key.replace(" ", "") == k:
            # print(key, value)
            return value

def generate_random_string(length):
    characters = '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(characters) for _ in range(length))

def generate_random_upper_string(length):
    characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return ''.join(random.choice(characters) for _ in range(length))



def file_rename(directory):

    def contains_chinese(text):
        return any('\u4e00' <= char <= '\u9fff' for char in text)

    try:
        index = 0
        for root, _, files in os.walk(directory):
            for file in files:
                old_file_path = os.path.join(root, file)
                # if contains_chinese(file):
                file_size = os.path.getsize(old_file_path)
                file_size_mb = file_size / (1024 * 1024)

                if file_size_mb < 50:
                    os.remove(old_file_path)
                    print(f"删除小文件: {old_file_path} (大小: {file_size_mb:.2f}MB)")
                    continue

                filename, ext = os.path.splitext(file)
                new_filename = "file_" +  str(index) + ext.lower()
                new_file_path = os.path.join(root, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"重命名: {old_file_path} -> {new_file_path}")
                index += 1
    except Exception as e:
        print(f"处理过程中发生错误: {e}")

'''
def get_current_process_usage():
    """获取当前进程的CPU和内存使用情况"""
    process = psutil.Process(os.getpid())

    # 获取CPU使用率（注意：需要在时间间隔内测量）
    cpu_percent = process.cpu_percent(interval=0.1)

    # 获取内存信息
    mem_info = process.memory_info()
    mem_full = process.memory_full_info()  # 需要psutil>=5.0

    return {
        'cpu_percent': cpu_percent,
        'memory_rss': mem_info.rss,  # 常驻内存
        'memory_vms': mem_info.vms,  # 虚拟内存
        'memory_uss': getattr(mem_full, 'uss', 0),  # 独立内存集（Linux/macOS）
        'memory_pss': getattr(mem_full, 'pss', 0),  # 比例内存集（Linux）
        'memory_percent': process.memory_percent()
    }

# 使用示例
current_usage = get_current_process_usage()
print(f"当前进程CPU使用率: {current_usage['cpu_percent']}%")
print(f"内存使用: {current_usage['memory_rss']/1024/1024:.2f} MB (RSS)")

def get_current_process_gpu_usage():
    """获取当前进程的GPU使用情况"""
    nvmlInit()
    device_count = nvmlDeviceGetCount()
    current_pid = os.getpid()
    gpu_usage = []

    for i in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        processes = nvmlDeviceGetComputeRunningProcesses(handle)

        for proc in processes:
            if proc.pid == current_pid:
                mem_info = nvmlDeviceGetMemoryInfo(handle)
                gpu_usage.append({
                    'gpu_id': i,
                    'used_memory': proc.usedGpuMemory,
                    'memory_percent': (proc.usedGpuMemory / mem_info.total) * 100
                })

    nvmlShutdown()
    return gpu_usage
# 使用示例
gpu_usage = get_current_process_gpu_usage()
if gpu_usage:
    for gpu in gpu_usage:
        print(f"GPU {gpu['gpu_id']}: 使用显存 {gpu['used_memory']/1024/1024:.2f} MB ({gpu['memory_percent']:.1f}%)")
else:
    print("当前进程没有使用GPU")
    
'''

class SB:
    def __init__(self):
        self.a = 1
        self.b = ""


if __name__ == '__main__':
    sb = SB()
    print(sb.a)
    print(sb.b)

    # get_cookie_key(
    #     ""
    #     "UIFID"
    #     # "s_v_web_id"
    # )
    # file_rename("C:/Users/10463/Desktop/RVC20240604Nvidia/assets/weights/")

    pass
