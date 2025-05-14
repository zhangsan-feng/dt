import hashlib
from uuid import uuid4
from _platform.bilibili.bilibili_adapter import bilibili_adapter
from _platform.douyin.douyin_adapter import douyin_adapter
from _platform.hongshu.hongshu_adapter import hongshu_adapter
from application.service.process_manager import create


async def link_analysis(link, user_agent):
    uuid = str(uuid4())
    try:
        if "douyin" in link:
            # await douyin_adapter(link, user_agent)
            await create(douyin_adapter(link, user_agent), uuid, link)

        if "bilibili" in link:
            # await bilibili_adapter(link, user_agent)
            await create(bilibili_adapter(link, user_agent), uuid, link)

        if "xiaohongshu" in link or "xhslink" in link:
            # await hongshu_adapter(link, user_agent)
            await create(hongshu_adapter(link, user_agent), uuid, link)
    except Exception as e:
        print(e)
