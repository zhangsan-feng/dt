import asyncio
from _platform.bilibili.bilibili_live import bilibili_live


async def bilibili_adapter(link, user_agent):

    if "live.bilibili.com" in link:
        await bilibili_live(link, user_agent)



    pass


if __name__ == '__main__':
    asyncio.run(
        bilibili_adapter(
            "",
            ""
        )
    )