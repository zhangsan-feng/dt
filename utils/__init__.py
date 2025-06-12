import os
import re
import time
import random

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
                filename, ext = os.path.splitext(file)
                new_filename = "file_" +  str(index) + ext.lower()
                new_file_path = os.path.join(root, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"重命名: {old_file_path} -> {new_file_path}")
                index += 1
    except Exception as e:
        print(f"处理过程中发生错误: {e}")


if __name__ == '__main__':
    # get_cookie_key(
    #     ""
    #     "UIFID"
    #     # "s_v_web_id"
    # )

    pass