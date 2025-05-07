from fastapi import Request

from _platform.bilibili.bilibili_adapter import bilibili_adapter
from _platform.douyin.douyin_adapter import douyin_adapter
from utils import match_url
from utils.logger import logger


async def link_analysis_api(request: Request):
    json_body = await request.json()
    logger.info(json_body)
    link = json_body["link"]
    link = match_url(link)
    logger.info(link)
    user_agent = dict(request.headers)["user-agent"]
    try:
        if "douyin" in link:
            await douyin_adapter(link, user_agent)
        if "bilibili" in link:
            await bilibili_adapter(link, user_agent)
    except Exception as e:

        return {"code":200, "data":"error", "msg":""}

    return {"code":200, "data":"success", "msg":""}