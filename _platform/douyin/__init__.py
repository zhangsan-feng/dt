
from utils import word_analysis, max_index
from utils.download import download_file
from config import Config
from application.entity.record_entity import record_add

async def douyin_data_handler(obj, headers):
    video_link = None
    if "video" in obj:
        if "bit_rate" in obj["video"]:
            video_link = obj["video"]["bit_rate"]

    aweme_id      = obj["aweme_id"]
    author_id       = obj["author"]["sec_uid"]
    author        = obj["author"]["nickname"]
    image_link    = obj["images"] if obj["images"] else None
    music_link    = obj["music"] if obj["music"] else None
    audio_link    = obj["music"] if obj["music"] else None
    desc          = obj["desc"]
    headers       = headers

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
            await download_file(image_url, image_file, headers)
            record_obj["files"].append(config.resource_path + image_file.replace(config.save_path, ""))

            if "video" in image:

                video_file = file + word_analysis(image["uri"]) + word_analysis(desc) + ".mp4"
                video_url = image["video"]["play_addr"]["url_list"][-1]
                await download_file(video_url, video_file, headers)
                record_obj["files"].append(config.resource_path + video_file.replace(config.save_path, ""))

    if video_link:
        # video_file = file + gen_uid() + ".mp4"
        video_file = file + word_analysis(desc) + ".mp4"
        video_url = video_link[max_index(video_link, "bit_rate")]["play_addr"]["url_list"][-1]
        await download_file(video_url, video_file, headers)
        record_obj["files"].append(config.resource_path + video_file.replace(config.save_path, ""))

    if music_link:
        pass

    if audio_link:
        pass

    record_obj["files"] = ",".join(record_obj["files"])



    await record_add(record_obj)



async def douyin_live_handler(obj, headers):

    pass
