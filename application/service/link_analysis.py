import hashlib

from _platform.bilibili.bilibili_adapter import bilibili_adapter
from _platform.douyin.douyin_adapter import douyin_adapter
from application.service.process_manager import create


async def link_analysis(link, user_agent):
    uuid = hashlib.md5(link.encode('utf-8')).hexdigest()
    try:
        if "douyin" in link:
            # await douyin_adapter(link, user_agent)
            await create(douyin_adapter(link, user_agent), uuid, link)

        if "bilibili" in link:
            await create(bilibili_adapter(link, user_agent), uuid, link)

    except Exception as e:
        print(e)
