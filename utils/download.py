import os
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed



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

    print(f"current download file:{file_name} link:{link}")
    await fetch_and_save(link, file_name)


async def download_flv_stream(link, file_name, headers):
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def fetch_and_save(url, save_path):
        if os.path.exists(save_path):
            print("File exists, skipping download:", save_path)
            return
        try:
            async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=None) as client:
                async with client.stream("GET", url=url) as response:
                    response.raise_for_status()
                    # if not response.is_successful():
                    #     return
                    with open(save_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)
                    print(f"FLV stream saved: {save_path}")
        except Exception as e:
            print(f"下载失败: {e}")
            raise

    print(f"current download file:{file_name} link:{link}")
    await fetch_and_save(link, file_name)