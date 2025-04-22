from fastapi import Request
from _platform.douyin.douyin_adapter import douyin_adapter
from urils import match_url
from config import Config, logger


async def link_analysis(request: Request):
    config = Config()
    json_body = await request.json()
    logger.info(json_body)
    link = json_body["link"]
    link = match_url(link)
    logger.info(link)
    user_agent = request.headers["User-Agent"]

    if "douyin" in link:
        return await douyin_adapter(link, user_agent)