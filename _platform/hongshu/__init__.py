import os

from application.entity.download_record_entity import record_add
from config import Config
from utils import word_analysis
from utils.download import download_stream


async def hongshu_data_handler(obj, headers):
    video_list = None
    if "video" in obj[0]["note_card"]:
        video_list = obj[0]["note_card"]["video"]
    aweme_id = obj[0]["id"]
    title = word_analysis(obj[0]["note_card"]["title"])
    image_list = obj[0]["note_card"]["image_list"]
    author = word_analysis(obj[0]["note_card"]["user"]["nickname"])
    author_id = word_analysis(obj[0]["note_card"]["user"]["user_id"])

    config = Config()
    tmp_path =  config.hongshu_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)
    file = tmp_path + word_analysis(author) + "_" + aweme_id + "_"

    record_obj = {
        "aweme_id": aweme_id,
        "author": author,
        "author_id": author_id,
        "desc": title,
        "files":[]
    }

    if image_list:
        for data in image_list:
            image_file = file +  ".png"
            image_url = data["url_default"]
            await download_stream(image_url, image_file, headers)
            record_obj["files"].append(config.resource_path + image_file.replace(config.save_path, ""))

            if "stream" in data and "h264" in data["stream"]:
                video_file = file + ".mp4"
                video_url = data["stream"]["h264"][0]["master_url"]
                await download_stream(video_url, video_file, headers)
                record_obj["files"].append(config.resource_path + video_file.replace(config.save_path, ""))

    if video_list:
        video_file = file + ".mp4"
        video_url = video_list["media"]["stream"]["h264"][0]["master_url"]
        await download_stream(video_url, video_file, headers)
        record_obj["files"].append(config.resource_path + video_file.replace(config.save_path, ""))

    record_obj["files"] = ",".join(record_obj["files"])
    await record_add(record_obj)

