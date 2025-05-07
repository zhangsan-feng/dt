from application.entity.record_entity import record_add
from config import Config
from utils import word_analysis, gen_uid
from utils.download import download_flv_stream


async def bilibili_data_handler():
    pass


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
    await download_flv_stream(flv_stream_url, file, headers)