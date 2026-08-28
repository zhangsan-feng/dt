import os
import subprocess
from config import Configuration
from utils import word_analysis, gen_uid
from utils.download import download_stream, download_stream


async def bilibili_data_handler(obj, author, title, aweme_id, author_id, headers):
    config = Configuration()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.bilibili_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)
    file = tmp_path + word_analysis(author) + "_" + word_analysis(title) + "_" + str(aweme_id)

    audio_file = file + ".mp3"
    video_file = file + ".mp4"
    merge_file = file + "merge.mp4"

    audio_url = obj['audio'][0]['baseUrl']
    await download_stream(audio_url, audio_file, headers)
    # video_url = obj['video'][0]['baseUrl']
    # await download_stream(video_url, video_file, headers)

    # record_obj["files"] = ",".join(record_obj["files"])
    # await record_add(record_obj)

    # command = [
    #     "ffmpeg", "-y", "-i", video_file, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-strict",
    #     "experimental", "-map", "0:v:0", "-map", "1:a:0", "-shortest", merge_file
    # ]
    # subprocess.run(command, check=True)


async def bilibili_live_handler(author, title, flv_stream_url, headers):
    config = Configuration()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.bilibili_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)
    file = tmp_path + word_analysis(author) + "_" + word_analysis(title) + "_" + gen_uid() + ".flv"

    headers["referer"] = flv_stream_url
    await download_stream(flv_stream_url, file, headers)
