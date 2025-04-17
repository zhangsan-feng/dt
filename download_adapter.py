from tenacity import retry, stop_after_attempt, wait_fixed
import httpx
import os
from entity.config_enetity import config
from urils import *


async def download_file(obj_dict):
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
    async def fetch_and_save(url, save_path):
        if os.path.exists(save_path):
            print("file exists skit download: ", save_path)
            return
        try:
            async with httpx.AsyncClient(headers=obj_dict.get("headers"), follow_redirects=True, timeout=10) as client:
                async with client.stream("GET", url=url) as response:
                    with open(save_path, "wb") as f:
                        async for chunk in response.aiter_bytes():
                            f.write(chunk)
                print(f"current download file save : {save_path}")
        except Exception as e:
            print(f"下载失败: {e}")
            raise

    file = config.platform(obj_dict.get("platform")) + word_analysis(obj_dict.get("author")) + "_" + obj_dict.get("aweme_id") + "_"
    image_link = obj_dict.get("image_link")
    video_link = obj_dict.get("video_link")
    audio_link = obj_dict.get("audio_link")
    music_link = obj_dict.get("music_link")
    live_link = obj_dict.get("live_link")

    if video_link:
        # video_file = file + gen_uid() + ".mp4"
        video_file = file + word_analysis(obj_dict.get("desc")) + ".mp4"
        video_url = video_link[max_index(video_link, "bit_rate")]["play_addr"]["url_list"][-1]
        await fetch_and_save(video_url, video_file)

    if image_link:
        for image in image_link:
            image_file = file + word_analysis(image["uri"]) + ".png"
            image_url = image["url_list"][-1]
            await fetch_and_save(image_url, image_file)

    if audio_link:
        pass

    if music_link:
        pass

    if live_link:
        pass



