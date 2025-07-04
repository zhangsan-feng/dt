import os
import time

import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from utils.errors import ProcessExit
from application.entity.config_entity import ConfigEntityObject




async def download_stream(link, file_name, headers):
    c = ConfigEntityObject()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def fetch_and_save(url, save_path):
        if os.path.exists(save_path):
            print("File exists, skipping download:", save_path)
            return
        try:
            async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=5) as client:
                async with client.stream("GET", url=url) as response:
                    response.raise_for_status()
                    # if not response.is_successful():
                    #     return
                    with open(save_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)
                    print(f"file saved to: {save_path}")
        except Exception as e:
            print(f"下载失败: {e} file:{save_path} link:{link}")
            raise


    if c.only_video and ".mp4" not in file_name: return
    if c.only_audio and ".mp3" not in file_name: return
    if c.only_image and ".png" not in file_name: return
    if c.download_delay: time.sleep(c.download_delay_num)

    if c.download_limit :
        directory  = os.path.dirname(file_name)
        mp3_count = sum(1 for f in os.listdir(directory) if f.lower().endswith('.mp3'))
        mp4_count = sum(1 for f in os.listdir(directory) if f.lower().endswith('.mp4'))
        if max(mp3_count, mp4_count) > c.download_limit_num:
            raise ProcessExit("download max exit")

    if c.download_format:
        end = file_name.split('.')[-1]
        f = file_name.split('_')[:2]
        t = "".join(f) + "." + end
        # print("file_format",t)
        file_name =  t

    if c.download_filter:
        pass


    print(f"current download file:{file_name} link:{link}")
    await fetch_and_save(link, file_name)

