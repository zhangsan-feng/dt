from entity.config_enetity import config
from fastapi import Request
import json


async def config_edit(request: Request):
    res = await request.json()

    config.douyin_cookie = res["douyin_cookie"] if "douyin_cookie" in res else None

    with open("../config.json", "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "douyin_cookie": res["douyin_cookie"],
            "weibo_cookie": res["douyin_cookie"],
            "bilibili_cookie": res["douyin_cookie"],
            "kuaishou_cookie": res["douyin_cookie"],
            "hongshu_cookie": res["douyin_cookie"],
            "save_path":config.save_path
        }, ensure_ascii=False, indent=4))

    return {
        "code": 200,
        "data": "success",
        "msg": ""
    }


async def config_query():
    return {
        "code": 200,
        "data": {
            "douyin_cookie": config.douyin_cookie,
            "save_path": config.save_path,
        },
        "msg": ""
    }
