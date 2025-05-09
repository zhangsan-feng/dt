import os
import subprocess
from application.entity.download_record_entity import record_add
from config import Config
from utils import word_analysis, gen_uid
from utils.download import download_stream, download_stream


async def bilibili_data_handler(obj, author, title, aweme_id, author_id, headers):
    config = Config()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))
    file = config.bilibili_path + word_analysis(author) + "_" + word_analysis(title)
    audio_file = file + "_" + ".mp3"
    video_file = file + "_" + ".mp4"
    merge_file = file + "_" + "merge.mp4"

    record_obj = {
        "aweme_id": aweme_id,
        "author": author,
        "author_id": author_id,
        "desc": title,
        "files": [
                    config.resource_path + audio_file.replace(config.save_path, ""),
                    config.resource_path + video_file.replace(config.save_path, ""),
                    config.resource_path + merge_file.replace(config.save_path, ""),
                  ]
    }
    record_obj["files"] = ",".join(record_obj["files"])
    await record_add(record_obj)

    audio_url = obj['audio'][0]['baseUrl']
    await download_stream(audio_url, audio_file, headers)
    video_url = obj['video'][0]['baseUrl']
    await download_stream(video_url, video_file, headers)

    command = [
        "ffmpeg", "-y", "-i", video_file, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental",
        "-map", "0:v:0", "-map", "1:a:0", "-shortest", merge_file
    ]
    subprocess.run(command, check=True)


async def bilibili_live_handler(author, title, flv_stream_url, headers):
    config = Config()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))
    file = config.bilibili_path + word_analysis(author) + "_" + word_analysis(title) + "_" + gen_uid() + ".flv"
    record_obj = {
        "aweme_id": "NULL",
        "author": author,
        "author_id": "NULL",
        "desc": title,
        "files": [config.resource_path + file.replace(config.save_path, "")]
    }
    record_obj["files"] = ",".join(record_obj["files"])
    await record_add(record_obj)
    headers["referer"] = flv_stream_url
    await download_stream(flv_stream_url, file, headers)