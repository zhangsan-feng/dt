import os

from utils import word_analysis, max_index, gen_uid
from utils.download import download_stream, download_stream
from config import Config
from application.entity.download_record_entity import record_add





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
    desc          = obj["desc"]


    config = Config()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.douyin_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)

    file = tmp_path + word_analysis(author) + "_" + aweme_id + "_"

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
        if len(music_link["play_url"]["url_list"]) == 0:
            return
        music_file = file + word_analysis(desc) + ".mp3"
        music_url = music_link["play_url"]["url_list"][-1]
        await download_stream(music_url, music_file, headers)
        record_obj["files"].append(config.resource_path + music_file.replace(config.save_path, ""))


    record_obj["files"] = ",".join(record_obj["files"])
    await record_add(record_obj)



async def douyin_live_handler(author, title, flv_stream_url, headers):
    config = Config()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.douyin_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)
    file = tmp_path + word_analysis(author) + "_" + word_analysis(title) + "_" + gen_uid() + ".flv"

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



"""
https://www.douyin.com/user/MS4wLjABAAAA3XNy70giFoK4bZR8JKmEZrkyI66yAsQvv1UROAILi24      麻勒勒
https://www.douyin.com/user/MS4wLjABAAAAhCtbaJTjDpUmAQNGhihHx_hrobOL5IWSXEKGVTgoUOc      阿七
https://www.douyin.com/user/MS4wLjABAAAApn56Ol39XDQxiaZQOR2I-yaVKoAqJhzKeT2h3jOlpFI      失眠熊
https://www.douyin.com/user/MS4wLjABAAAAt37t_G9YHe7o1uQC8RmnYwOw14BQs59ocZyKMbNb2TkHVVmnEp7cDmzIRzF3gWTG 来点宫酱w
https://www.douyin.com/user/MS4wLjABAAAA4cH-PrI9IbWVUxmcv9h30vV8FMwdTgdmp4-XnLWtlEQ         别捏七七脸
https://www.douyin.com/user/MS4wLjABAAAAA7tqSFYdDSagFkE_SpWiGRphlbgCyQ4iIxLOMpTkdV0     小花花花儿
https://www.douyin.com/user/MS4wLjABAAAAfl8D63aFQdpcZc5oUbGPR_Wr7cZl2P66bduaJZT5FszPzpabcLECCDOVt2Y-0xUT    元呆呆
https://www.douyin.com/user/MS4wLjABAAAA0Wk4gxp3AYFnqoqo-IBF6lbdLnrxgjy__DdhPBNBkws  封茗囧菌
https://www.douyin.com/user/MS4wLjABAAAA9V4sakBw8N5agTXKhE0imOs3gDF-3ehe_HcAaVeWZJw     娜娜酱要翻倍
https://www.douyin.com/user/MS4wLjABAAAArrr6419gq2wn5M8Oy5qRTfZ6GhpIsbd1fmxvT27uMr8     丸子yooo

"""