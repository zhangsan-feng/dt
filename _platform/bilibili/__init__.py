import os
import subprocess
from application.entity.record_entity import record_add
from application.entity.config_entity import ConfigEntityObject
from utils import word_analysis, gen_uid
from utils.download import download_stream, download_stream


async def bilibili_data_handler(obj, author, title, aweme_id, author_id, headers):
    config = ConfigEntityObject()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.bilibili_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)
    file = tmp_path + word_analysis(author) + "_" + word_analysis(title) + "_" + str(aweme_id)

    audio_file = file + ".mp3"
    video_file = file + ".mp4"
    merge_file = file + "merge.mp4"

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


    audio_url = obj['audio'][0]['baseUrl']
    await download_stream(audio_url, audio_file, headers)
    video_url = obj['video'][0]['baseUrl']
    await download_stream(video_url, video_file, headers)

    record_obj["files"] = ",".join(record_obj["files"])
    await record_add(record_obj)

    command = [
        "ffmpeg", "-y", "-i", video_file, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", "-strict",
        "experimental", "-map", "0:v:0", "-map", "1:a:0", "-shortest", merge_file
    ]
    subprocess.run(command, check=True)


async def bilibili_live_handler(author, title, flv_stream_url, headers):
    config = ConfigEntityObject()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.bilibili_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)
    file = tmp_path + word_analysis(author) + "_" + word_analysis(title) + "_" + gen_uid() + ".flv"

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