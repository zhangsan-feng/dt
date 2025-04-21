import re
import time
import random

from sqlalchemy.sql.coercions import expect
from tenacity import retry, stop_after_attempt, wait_fixed
import httpx
import os



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
    if len(text) > 20:
        return text[:20]
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


class HttpRequest:
    def __init__(self, url, params, proxy, headers):
        self.url = url
        self.params = params
        self.proxy = proxy
        self.headers = headers

    async def httpx_get(self):
        async def _get_():
            try:
                async with httpx.AsyncClient() as client:
                    return await client.get(self.url, params=self.params, headers=self.headers)
            except Exception as e:
                print(f"下载失败: {e}")
                raise
        await _get_()
    def httpx_post(self):
        pass
    def aiohttp_get(self):
        pass
    def aiohttp_post(self):
        pass


async def download_file(link, file_name, headers):
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def fetch_and_save(url, save_path):
        if os.path.exists(save_path):
            print("file exists skit download: ", save_path)
            return
        try:
            async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=10) as client:
                async with client.stream("GET", url=url) as response:
                    with open(save_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)
                print(f"current download file save : {save_path}")
        except Exception as e:
            print(f"下载失败: {e}")
            raise

    await fetch_and_save(link, file_name)
