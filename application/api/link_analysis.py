from fastapi import Request
from _platform.douyin.douyin_adapter import douyin_adapter
from utils import match_url
from utils.logger import logger


async def link_analysis_api(request: Request):
    json_body = await request.json()
    logger.info(json_body)
    link = json_body["link"]
    link = match_url(link)
    logger.info(link)
    user_agent = request.headers["User-Agent"]

    if "douyin" in link:
        await douyin_adapter(link, user_agent)

    return {"code":200, "data":"", "msg":""}