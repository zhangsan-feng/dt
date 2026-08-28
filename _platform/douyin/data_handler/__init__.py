import os
from utils import word_analysis, max_index, gen_uid
from utils.download import  download_stream
from config import Configuration



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


    config = Configuration()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.douyin_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)

    file = tmp_path + word_analysis(author) + "_" + aweme_id + "_"

    if image_link:
        for image in image_link:
            image_file = file + word_analysis(image["uri"]) + ".png"
            image_url = image["url_list"][-1]
            await download_stream(image_url, image_file, headers)

            if "video" in image:
                video_file = file + word_analysis(image["uri"]) + word_analysis(desc) + ".mp4"
                video_url = image["video"]["play_addr"]["url_list"][-1]
                await download_stream(video_url, video_file, headers)

    if video_link:
        video_file = file + word_analysis(desc) + ".mp4"
        video_url = video_link[max_index(video_link, "bit_rate")]["play_addr"]["url_list"][-1]
        await download_stream(video_url, video_file, headers)

    if music_link:
        if len(music_link["play_url"]["url_list"]) == 0:
            return
        music_file = file + word_analysis(desc) + ".mp3"
        music_url = music_link["play_url"]["url_list"][-1]
        await download_stream(music_url, music_file, headers)



async def douyin_live_handler(author, title, flv_stream_url, headers):
    config = Configuration()
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    tmp_path =  config.douyin_path + "/" + word_analysis(author) + "/"
    if not os.path.exists(tmp_path):os.mkdir(tmp_path)
    file = tmp_path + word_analysis(author) + "_" + word_analysis(title) + "_" + gen_uid() + ".flv"

    headers["referer"] = flv_stream_url
    await download_stream(flv_stream_url, file, headers)
