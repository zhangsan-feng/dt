
from download_adapter import  download_file




async def douyin_data_handler(obj, headers):
    video_link = None
    if "video" in obj:
        if "bit_rate" in obj["video"]:
            video_link = obj["video"]["bit_rate"]

    obj_dict = {
        "aweme_id"      : obj["aweme_id"],
        "user_id"       : obj["author"]["sec_uid"],
        "author"        : obj["author"]["nickname"],
        "video_link"    : video_link,
        "image_link"    : obj["images"] if obj["images"] else None,
        "music_link"    : obj["music"] if obj["music"] else None,
        "desc"          : obj["desc"],
        "platform"      : "douyin",
        "headers"       : headers,
    }
    # print(json.dumps(obj_dict, indent=4, ensure_ascii=False))

    await download_file(obj_dict)


async def douyin_live_handler(obj, headers):

    pass
