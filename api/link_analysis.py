
from fastapi import Request
from _platform.douyin.douyin_adapter import douyin_adapter
from urils import match_url



async def link_analysis(request: Request):
    json_body = await request.json()
    print(json_body)
    link = json_body["link"]
    link = match_url(link)
    print(link)
    user_agent = request.headers["User-Agent"]

    if "douyin" in link:
        return await douyin_adapter(link, user_agent)