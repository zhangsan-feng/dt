import os

from utils import word_analysis, max_index, gen_uid
from utils.download import download_stream, download_stream
from config import Config
from application.entity.download_record_entity import record_add


def author_path(author):

    # tmp_path =  config.douyin_path + "/" + word_analysis(author) + "/"
    # if os.path.exists(tmp_path):os.mkdir(tmp_path)

    pass


async def douyin_data_handler(obj, headers):
    video_link = None
    if "video" in obj:
        if "bit_rate" in obj["video"]:
            video_link = obj["video"]["bit_rate"]

    aweme_id      = obj["aweme_id"]
    author_id     = obj["author"]["sec_uid"]
    author        = obj["author"]["nickname"]
    image_link    = obj["images"] if "images" in obj else None
    music_link    = obj["music"] if "music" in obj else None
    audio_link    = obj["music"] if obj["music"] else None
    desc          = obj["desc"]


    config = Config()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    file = config.douyin_path + word_analysis(author) + "_" + aweme_id + "_"

    record_obj = {
        "aweme_id": aweme_id,
        "author": author,
        "author_id": author_id,
        "desc": desc,
        "files":[]
    }

    if image_link:
        for image in image_link:
            image_file = file + word_analysis(image["uri"]) + ".png"
            image_url = image["url_list"][-1]
            await download_stream(image_url, image_file, headers)
            record_obj["files"].append(config.resource_path + image_file.replace(config.save_path, ""))

            if "video" in image:
                video_file = file + word_analysis(image["uri"]) + word_analysis(desc) + ".mp4"
                video_url = image["video"]["play_addr"]["url_list"][-1]
                await download_stream(video_url, video_file, headers)
                record_obj["files"].append(config.resource_path + video_file.replace(config.save_path, ""))

    if video_link:
        video_file = file + word_analysis(desc) + ".mp4"
        video_url = video_link[max_index(video_link, "bit_rate")]["play_addr"]["url_list"][-1]
        await download_stream(video_url, video_file, headers)
        record_obj["files"].append(config.resource_path + video_file.replace(config.save_path, ""))

    if music_link:
        music_file = file + word_analysis(desc) + ".mp3"
        music_url = music_link["play_url"]["url_list"][-1]
        await download_stream(music_url, music_file, headers)
        record_obj["files"].append(config.resource_path + music_file.replace(config.save_path, ""))

    if audio_link:
        pass

    record_obj["files"] = ",".join(record_obj["files"])
    await record_add(record_obj)



async def douyin_live_handler(author, title, flv_stream_url, headers):
    config = Config()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))
    file = config.douyin_path + word_analysis(author) + "_" + word_analysis(title) + "_" + gen_uid() + ".flv"
    record_obj = {
        "aweme_id": "NULL",
        "author": author,
        "author_id": "NULL",
        "desc": title,
        "files":[config.resource_path + file.replace(config.save_path, "")]
    }
    record_obj["files"] = ",".join(record_obj["files"])
    await record_add(record_obj)
    headers["referer"] = flv_stream_url
    await download_stream(flv_stream_url, file, headers)

