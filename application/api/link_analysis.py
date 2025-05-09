

from fastapi import Request
from utils import match_url
from utils.logger import logger
from application.service.link_analysis import link_analysis


async def link_analysis_api(request: Request):
    json_body = await request.json()
    logger.info(json_body)
    link = json_body["link"]
    link = match_url(link)
    logger.info(link)
    user_agent = dict(request.headers)["user-agent"]

    await link_analysis(link, user_agent)


    return {"code":200, "data":"已经加入下载队列", "msg":""}