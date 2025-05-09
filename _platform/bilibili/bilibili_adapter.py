import asyncio

from _platform.bilibili.bilibili_detail import bilibili_detail
from _platform.bilibili.bilibili_live import bilibili_live
from config import Config

async def bilibili_adapter(link, user_agent):
    config = Config()

    if "live.bilibili.com" in link:
        await bilibili_live(link, user_agent)

    if "bilibili.com/video" in link:
        bvid = link.split("?")[0].replace("https://www.bilibili.com/video/", "")
        await bilibili_detail(bvid, user_agent, "")


    pass


if __name__ == '__main__':
    asyncio.run(
        bilibili_adapter(
            "",
            ""
        )
    )