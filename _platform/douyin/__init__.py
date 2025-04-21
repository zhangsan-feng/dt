
from urils import *
config = ""


async def douyin_data_handler(obj, headers):
    video_link = None
    if "video" in obj:
        if "bit_rate" in obj["video"]:
            video_link = obj["video"]["bit_rate"]

    aweme_id      = obj["aweme_id"]
    user_id       = obj["author"]["sec_uid"]
    author        = obj["author"]["nickname"]
    video_link    = video_link
    image_link    = obj["images"] if obj["images"] else None
    music_link    = obj["music"] if obj["music"] else None
    audio_link    = obj["music"] if obj["music"] else None
    desc          = obj["desc"]
    headers       = headers


    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))
    file = config.douyin_path + word_analysis(author) + "_" + aweme_id + "_"

    if image_link:
        for image in image_link:
            image_file = file + word_analysis(image["uri"]) + ".png"
            image_url = image["url_list"][-1]
            await download_file(image_url, image_file, headers)

            if "video" in image:
                print(image["video"])
                video_file = file + word_analysis(desc) + ".mp4"
                video_url = image["video"]["play_addr"]["url_list"][-1]
                await download_file(video_url, video_file, headers)

    if video_link:
        # video_file = file + gen_uid() + ".mp4"
        video_file = file + word_analysis(desc) + ".mp4"
        video_url = video_link[max_index(video_link, "bit_rate")]["play_addr"]["url_list"][-1]
        await download_file(video_url, video_file, headers)




async def douyin_live_handler(obj, headers):

    pass
